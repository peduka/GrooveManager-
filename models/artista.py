class Artista:
    def __init__(self, nome, pais_origem="Desconhecido"):
        self.__nome = nome
        self.__pais_origem = pais_origem

    @property
    def nome(self):
        return self.__nome

    @property
    def pais_origem(self):
        return self.__pais_origem