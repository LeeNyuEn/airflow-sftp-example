from typing import Union

from airflow.providers.sftp.hooks.sftp import SFTPHook
from paramiko import SFTPClient, Transport

from airflow_example.lib.source.base import DataSourceManager
from airflow_example.plugins.sftp import SftpManager


class SftpDataSourceManager(DataSourceManager, SftpManager):
    def fetch_data(self):
        # Logic to fetch data from SFTP source
        print("Fetching data from SFTP")
