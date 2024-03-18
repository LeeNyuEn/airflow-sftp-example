from airflow_example.lib.source.base import DataSourceManager
from airflow_example.lib.connections.sftp import SftpManager


class SftpDataSourceManager(DataSourceManager, SftpManager):
    def fetch_data(self):
        # Logic to fetch data from SFTP source
        print("Fetching data from SFTP")
