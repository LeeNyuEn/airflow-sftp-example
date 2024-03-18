from airflow_example.lib.target.base import DataTargetManager
from airflow_example.lib import sftp


class SftpDataTargetManager(DataTargetManager, sftp.SftpManager):
    def ingest_data(self):
        # Logic to ingest data into Google Cloud Storage
        print("Ingesting data into SFTP Server")
