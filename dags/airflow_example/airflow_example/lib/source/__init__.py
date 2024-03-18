from airflow_example.lib.source.sftp import SftpDataSourceManager


class DataSourceManagerFactory:
    @staticmethod
    def create_source_manager(source_type, **kwargs):
        if source_type == "sftp":
            return SftpDataSourceManager(**kwargs)
        else:
            raise ValueError(f"{source_type} is not supported")
