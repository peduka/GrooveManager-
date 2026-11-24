from models.midia import Midia


class CD(Midia):

    OPCOES_CONSERVACAO = ["Lacrado", "Excelente", "Bom", "Ruim"]

    # RELAÇÃO DE AGREGAÇÃO: 'artista' recebe um objeto instanciado de Artista
    def __init__(self, titulo, data_lancamento, artista, estado_conservacao, registro_compra):
        self.__titulo = titulo
        self.__data_lancamento = data_lancamento
        self.__artista = artista
        self.estado_conservacao = estado_conservacao

        # RELAÇÃO DE COMPOSIÇÃO: RegistroCompra só existe atrelado a esta mídia
        self.__registro_compra = registro_compra

    @property
    def titulo(self):
        return self.__titulo

    @property
    def data_lancamento(self):
        return self.__data_lancamento

    @property
    def artista(self):
        return self.__artista

    @property
    def registro_compra(self):
        return self.__registro_compra

    @property
    def estado_conservacao(self):
        return self.__estado_conservacao

    @estado_conservacao.setter
    def estado_conservacao(self, valor):
        if valor in CD.OPCOES_CONSERVACAO:
            self.__estado_conservacao = valor
        else:
            self.__estado_conservacao = "Não avaliado"
            print(f"Estado inválido. Use uma dessas opções: {CD.OPCOES_CONSERVACAO}")

    def exibir_ficha_tecnica(self):
        print("\n===== Ficha Técnica: CD =====")
        print(f"Título: {self.titulo}")
        print(f"Artista: {self.artista.nome}")
        print(f"Data de lançamento: {self.data_lancamento}")
        print(f"Estado de conservação: {self.estado_conservacao}")
        print(f"Valor pago: R$ {self.registro_compra.valor:.2f}")
        print(f"Data de prensagem: {self.registro_compra.data_prensagem}")
        print(f"Local de prensagem: {self.registro_compra.local_prensagem}")