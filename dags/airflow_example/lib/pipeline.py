import abc
from typing import Dict, List, Union

import time

from airflow_example.lib.source import DataSourceManagerFactory
from airflow_example.lib.target import DataTargetManagerFactory
from airflow_example.lib.transform.base import DataTransformer
from airflow_example.utils import list_util
from config import settings


class DataPipeline(abc.ABC):
    """
    DataPipeline
    ============

    Abstract class for managing pipeline processes from source to target.

    This class provides an interface for implementing pipeline processes that involve transferring data from a source to a target.
    """

    def __init__(
        self,
        source_type: str,
        target_type: str,
        source_config: Dict,
        target_config: Dict,
        transformer=None,
    ):
        self.source_manager = DataSourceManagerFactory.create_source_manager(
            source_type, **source_config
        )
        self.target_manager = DataTargetManagerFactory.create_target_manager(
            target_type, **target_config
        )
        self.transformer = transformer

    @abc.abstractmethod
    def run(self):
        pass


class SftpFileTransferPipeline(DataPipeline):
    """
    SftpFileTransferPipeline
    =========================

    Class for managing file transfers with SFTP servers.

    This class facilitates secure file transfer to and from SFTP servers.
    """

    _CHUNK_SIZE = 32768
    _RETRY_DELAY = 10
    _MAX_RETRIES = 3
    _CHUNK_SIZE = settings.sftp_default_config.chunk_size
    _RETRY_DELAY = settings.sftp_default_config.retry_delay
    _MAX_RETRIES = settings.sftp_default_config.max_retries

    def __init__(
        self,
        source_config: Dict,
        target_config: Dict,
        transformer: DataTransformer = None,
    ):
        super().__init__("sftp", "sftp", source_config, target_config, transformer)

    def __create_directory(self, directories: Union[List[str], None] = None) -> None:
        if directories:
            self.target_manager.create_directory_recursive(directories)
        else:
            print(f"No directory needed to create")

    def __transfer_files(
        self,
        source_file_path: str,
        target_file_path: Union[str, None] = None,
    ):
        target_file_path = target_file_path if target_file_path else source_file_path
        retries = 0
        while True:
            try:
                chunks = self.source_manager.fetch_data(
                    source_file_path, SftpFileTransferPipeline._CHUNK_SIZE
                )
                self.target_manager.ingest_data(target_file_path, chunks)
                break  # Break the loop if transfer is successful
            except Exception as e:
                print(f"Error: {e}")
                retries += 1
                if retries == SftpFileTransferPipeline._MAX_RETRIES:
                    print("Max retries reached. Could not complete the operation.")
                    raise Exception("Max retries reached")
                print(f"Retrying in {SftpFileTransferPipeline._RETRY_DELAY} seconds...")
                time.sleep(SftpFileTransferPipeline._RETRY_DELAY)
                continue

    def run(self):
        self.source_manager.get_sftp_client()
        self.target_manager.get_sftp_client()

        source_file_paths, source_directory = self.source_manager.list_files()
        target_file_paths, target_directory = self.target_manager.list_files()
        files_to_put = list_util.not_in(source_file_paths, target_file_paths)
        directory_to_create = list_util.not_in(source_directory, target_directory)

        print(f"Files need to put: {files_to_put}")
        print(f"Directory need to create: {directory_to_create}")

        self.__create_directory(directory_to_create)

        for file in files_to_put:
            self.__transfer_files(source_file_path=file)

        self.source_manager.close_connection()
        self.target_manager.close_connection()
