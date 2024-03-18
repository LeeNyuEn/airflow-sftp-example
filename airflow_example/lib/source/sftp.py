from airflow_example.lib.source.base import DataSourceManager


class SftpDataSourceManager(DataSourceManager):
    def __init__(self, *, host=None, username=None, password=None, hook=None):
        self.host = host
        self.username = username
        self.password = password
        self.hook = hook

    def fetch_data(self):
        # Logic to fetch data from SFTP source
        print("Fetching data from SFTP")
