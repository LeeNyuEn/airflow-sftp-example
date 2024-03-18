import abc


class DataTransformer(abc.ABC):
    @abc.abstractmethod
    def transform(self, data):
        pass
