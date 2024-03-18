import abc


class DataSourceManager(abc.ABC):
    @abc.abstractmethod
    def fetch_data(self):
        pass
