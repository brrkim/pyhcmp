from abc import *

class Provisioning(metaclass=ABCMeta):
    @abstractmethod
    def create(self,**kwargs):
        pass
    @abstractmethod
    def read(self,**kwargs):
        pass
    @abstractmethod
    def update(self,**kwargs):
        pass
    @abstractmethod
    def delete(self,**kwargs):
        pass

class Management(metaclass=ABCMeta):
    @abstractmethod
    def start(self,**kwargs):
        pass
    @abstractmethod
    def stop(self,**kwargs):
        pass
    @abstractmethod
    def restart(self,**kwargs):
        pass

class Associate(metaclass=ABCMeta):
    @abstractmethod
    def attach(self,**kwargs):
        pass
    @abstractmethod
    def detach(self,**kwargs):
        pass