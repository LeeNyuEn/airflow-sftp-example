from datetime import timedelta

import pendulum
from airflow.providers.sftp.hooks.sftp import SFTPHook
from airflow.decorators import dag, task


@dag(
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=10),
    },
    schedule="@hourly",
    start_date=pendulum.datetime(2024, 3, 18, tz="UTC"),
    catchup=False,
    tags=["etl", "sftp"],
)
def file_transfer():
    from airflow_example.lib.pipeline import SftpFileTransferPipeline

    @task
    def sftp_file_transfer(source_directory, target_directory):
        sftp_transfer_pipeline = SftpFileTransferPipeline(
            source_config={
                "hook": SFTPHook(
                    ssh_conn_id="sftp_source",
                ),
                "directory": source_directory,
            },
            target_config={
                "hook": SFTPHook(
                    ssh_conn_id="sftp_target",
                ),
                "directory": target_directory,
            },
        )
        sftp_transfer_pipeline.run()

    sftp_file_transfer(
        source_directory="{{var.json.dag_file_transfer_config.sftp_source.directory}}",
        target_directory="{{var.json.dag_file_transfer_config.sftp_target.directory}}",
    )


file_transfer()
