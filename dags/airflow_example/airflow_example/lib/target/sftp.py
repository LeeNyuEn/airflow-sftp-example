from airflow_example.lib.target.base import DataTargetManager
from airflow_example.plugins.sftp import SftpManager


class SftpDataTargetManager(SftpManager, DataTargetManager):
    def ingest_data(self):
        # Logic to ingest data into Google Cloud Storage
        print("Ingesting data into SFTP Server")
