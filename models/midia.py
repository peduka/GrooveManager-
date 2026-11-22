from abc import ABC, abstractmethod


class Midia(ABC):

    @property
    @abstractmethod
    def titulo(self):
        pass

    @property
    @abstractmethod
    def data_lancamento(self):
        pass

    @abstractmethod
    def exibir_ficha_tecnica(self):
        pass

    @property
    @abstractmethod
    def artista(self):
        pass

    @property
    @abstractmethod
    def estado_conservacao(self):
        pass

    

