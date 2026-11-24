class RegistroCompra:

    def __init__(self, valor, data_prensagem, local_prensagem):
        self.valor = valor
        self.__data_prensagem = data_prensagem
        self.__local_prensagem = local_prensagem

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, novo_valor):
        try:
            valor_convertido = float(str(novo_valor).replace(",", "."))
        except (ValueError, TypeError):
            raise ValueError("O valor pago deve ser um número válido.")

        if valor_convertido < 0:
            raise ValueError("O valor pago não pode ser negativo.")

        self.__valor = valor_convertido

    @property
    def data_prensagem(self):
        return self.__data_prensagem

    @property
    def local_prensagem(self):
        return self.__local_prensagem