import abc
from typing import Dict, List, Union

from airflow_example.lib.source import DataSourceManagerFactory
from airflow_example.lib.target import DataTargetManagerFactory
from airflow_example.lib.transform.base import DataTransformer
from airflow_example.utils import list_util


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

    def run(self):
        source_file_paths, source_directory = self.source_manager.list_files()
        target_file_paths, target_directory = self.target_manager.list_files()
        files_to_put = list_util.not_in(source_file_paths, target_file_paths)
        directory_to_create = list_util.not_in(source_directory, target_directory)
        print(files_to_put)
        print(directory_to_create)
        self.__create_directory(directory_to_create)
