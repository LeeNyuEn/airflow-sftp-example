from google.cloud import storage
from airflow_example.lib.source import DataSourceManagerFactory

from airflow_example.lib.source.base import DataSourceManager
from airflow_example.lib.target import DataTargetManagerFactory


class DataPipeline:
    def __init__(
        self, source_type, target_type, source_config, target_config, transformer=None
    ):
        self.source_manager = DataSourceManagerFactory.create_source_manager(
            source_type, **source_config
        )
        self.target_manager = DataTargetManagerFactory.create_target_manager(
            target_type, **target_config
        )
        self.transformer = transformer

    def transfer(self):
        data = self.source_manager.fetch_data()

        if self.transformer:
            data = self.transformer.transform(data)

        self.target_manager.ingest_data(data)
