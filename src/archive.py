from abc import ABC, abstractmethod


class Archive(ABC):
    @property
    @abstractmethod
    def modded(self):
        pass

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def initialize_spreadsheets(self, filename):
        pass

    @abstractmethod
    def load_spreadsheets(self):
        pass

    @abstractmethod
    def dump_spreadsheets(self):
        pass
