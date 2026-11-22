class RegistroCompra:

    def __init__(self, valor, data_prensagem, local_prensagem):
        self.__valor = valor
        self.__data_prensagem = data_prensagem
        self.__local_prensagem = local_prensagem

    @property
    def valor(self):
        return self.__valor

    @property
    def data_prensagem(self):
        return self.__data_prensagem

    @property
    def local_prensagem(self):
        return self.__local_prensagem