from abc import ABC, abstractmethod


class Midia(ABC):

    def __init__(self, titulo, data_lancamento, artista, estado_conservacao):
        self.titulo = titulo
        self.data_lancamento = data_lancamento
        self.artista = artista
        self.estado_conservacao = estado_conservacao

    @abstractmethod
    def exibir_ficha_tecnica(self):
        pass


    """
Versão 2 da classe Midia — com __init__ na classe base.

Diferença em relação à versão 1 (sem __init__):
- v1: cada subclasse implementa seu próprio __init__ e usa @property/setter
  com validação, oferecendo encapsulamento forte (atributos privados __).
- v2: a classe base já centraliza o __init__, tornando as subclasses mais
  enxutas (reaproveitamento de código), mas os atributos ficam públicos,
  sem validação — qualquer valor é aceito, mesmo inválido.
"""