from airflow_example.lib.source.base import DataSourceManager


class SftpDataSourceManager(DataSourceManager):
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def fetch_data(self):
        # Logic to fetch data from SFTP source
        print("Fetching data from SFTP")
