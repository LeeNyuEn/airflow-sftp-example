import time
import paramiko


class RetryDecorator:
    max_retries = 3
    delay = 1

    @classmethod
    def retry(cls, func):
        def wrapper(*args, **kwargs):
            retries = cls.max_retries
            while retries > 0:
                try:
                    return func(*args, **kwargs)
                except (paramiko.SSHException, IOError) as e:
                    print(f"Error: {e}")
                    retries -= 1
                    if retries == 0:
                        print("Max retries reached. Could not complete the operation.")
                        raise
                    print(f"Retrying in {cls.delay} seconds...")
                    time.sleep(cls.delay)

        return wrapper
