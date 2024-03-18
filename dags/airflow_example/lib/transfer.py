from time import sleep

from config import settings


def retrieve_file_in_chunks(
    source_hook, source_file_path, destination_hook, destination_file_path
):
    chunk_size = settings.chunk_size  # Adjust the chunk size as needed
    retry_delay = settings.retry_delay  # Seconds to wait before retrying
    max_retries = settings.max_retries  # Maximum number of retries

    with source_hook.get_conn() as source_conn:
        source_sftp = source_conn.open_sftp()
        source_file_size = source_sftp.stat(source_file_path).st_size

        with destination_hook.get_conn() as destination_conn:
            destination_sftp = destination_conn.open_sftp()

            last_position = 0
            retries = 0

            while last_position < source_file_size:
                try:
                    with source_sftp.open(source_file_path, "rb") as source_file:
                        source_file.seek(last_position)
                        chunk = source_file.read(chunk_size)

                        with destination_sftp.open(
                            destination_file_path, "ab"
                        ) as destination_file:
                            destination_file.write(chunk)

                        last_position = source_file.tell()

                except Exception as e:
                    print(f"Error: {e}")
                    retries += 1
                    if retries == max_retries:
                        print("Max retries reached. Could not complete the operation.")
                        raise Exception("Max retries reached")
                    print(f"Retrying in {retry_delay} seconds...")
                    sleep(retry_delay)
                    continue

                retries = 0  # Reset retry count if successful
