from airflow_example.lib.target.base import DataTargetManager


class SftpDataTargetManager(DataTargetManager):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def ingest_data(self, data):
        # Logic to ingest data into Google Cloud Storage
        print("Ingesting data into Google Cloud Storage")
