from airflow_example.lib.source.base import DataSourceManager
from airflow_example.lib import sftp


class SftpDataSourceManager(DataSourceManager, sftp.SftpManager):
    def fetch_data(self):
        # Logic to fetch data from SFTP source
        print("Fetching data from SFTP")
