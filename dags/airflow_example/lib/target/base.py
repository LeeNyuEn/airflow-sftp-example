import abc


class DataTargetManager(abc.ABC):
    @abc.abstractmethod
    def ingest_data(self, data):
        pass
