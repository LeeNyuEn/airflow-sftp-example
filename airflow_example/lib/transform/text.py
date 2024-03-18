# Example of implementing a specific data transformer
from airflow_example.lib.transform.base import DataTransformer


class SomeFanctyTransfromationHere(DataTransformer):
    """
    Class to define and handle fancy data trsnfromation
    """
    def transform(self):
        print("Doing some mythic transformation there!")
