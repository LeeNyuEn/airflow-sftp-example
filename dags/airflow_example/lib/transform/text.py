# Example of implementing a specific data transformer
from airflow_example.lib.transform.base import DataTransformer


class SomeFanctyTextTransfromationHere(DataTransformer):
    """
    Class to define and handle fancy data transformation
    """
    def transform(self):
        print("Doing some mythic transformation there!")
