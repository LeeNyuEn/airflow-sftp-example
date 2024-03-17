import abc
import boto3
from google.cloud import storage
import paramiko


class DataSourceManager(abc.ABC):
    @abc.abstractmethod
    def fetch_data(self):
        pass


class SftpDataSourceManager(DataSourceManager):
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def fetch_data(self):
        # Logic to fetch data from SFTP source
        print("Fetching data from SFTP")


class S3DataSourceManager(DataSourceManager):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3")

    def fetch_data(self):
        # Logic to fetch data from S3 source
        print("Fetching data from S3")


class GcsDataSourceManager(DataSourceManager):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.gcs_client = storage.Client()

    def fetch_data(self):
        # Logic to fetch data from Google Cloud Storage source
        print("Fetching data from Google Cloud Storage")


class DatabaseDataSourceManager(DataSourceManager):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        # Logic to establish connection to database

    def fetch_data(self):
        # Logic to fetch data from database
        print("Fetching data from Database")


class DataTargetManager(abc.ABC):
    @abc.abstractmethod
    def ingest_data(self, data):
        pass


class S3DataTargetManager(DataTargetManager):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3")

    def ingest_data(self, data):
        # Logic to ingest data into S3
        print("Ingesting data into S3")


class GcsDataTargetManager(DataTargetManager):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.gcs_client = storage.Client()

    def ingest_data(self, data):
        # Logic to ingest data into Google Cloud Storage
        print("Ingesting data into Google Cloud Storage")


class DataSourceManagerFactory:
    @staticmethod
    def create_source_manager(source_type, **kwargs):
        if source_type == "sftp":
            return SftpDataSourceManager(**kwargs)
        elif source_type == "s3":
            return S3DataSourceManager(**kwargs)
        elif source_type == "gcs":
            return GcsDataSourceManager(**kwargs)
        elif source_type == "database":
            return DatabaseDataSourceManager(**kwargs)


class DataTargetManagerFactory:
    @staticmethod
    def create_target_manager(target_type, **kwargs):
        if target_type == "s3":
            return S3DataTargetManager(**kwargs)
        elif target_type == "gcs":
            return GcsDataTargetManager(**kwargs)


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


if __name__ == "__main__":
    # Example usage:
    source_config = {
        "host": "sftp.example.com",
        "username": "user",
        "password": "password",
    }
    target_config = {"bucket_name": "my_bucket"}

    pipeline = DataPipeline(
        source_type="sftp",
        target_type="s3",
        source_config=source_config,
        target_config=target_config,
    )
    pipeline.transfer()
