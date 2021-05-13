from abc import *

class Provisioning(metaclass=ABCMeta):
    @abstractmethod
    def create(self):
        pass
    @abstractmethod
    def read(self):
        pass
    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def delete(self):
        pass

class Management(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        pass
    @abstractmethod
    def stop(self):
        pass
    @abstractmethod
    def restart(self):
        pass

class Associate(metaclass=ABCMeta):
    @abstractmethod
    def attach(self):
        pass
    @abstractmethod
    def detach(self):
        pass