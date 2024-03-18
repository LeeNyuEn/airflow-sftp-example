import abc
from typing import Dict

from airflow_example.lib.source import DataSourceManagerFactory
from airflow_example.lib.target import DataTargetManagerFactory


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
        transformer=None,
    ):
        super().__init__("sftp", "sftp", source_config, target_config, transformer)

    def run(self):
        print("Hello")