from models.artista import Artista


class Acervo:

    total_acervos_criados = 0  # público

    def __init__(self):
        self._midias = []                  # protegido

        # RELAÇÃO DE AGREGAÇÃO: o Acervo guarda os Artistas de forma
        # independente das mídias. Várias mídias podem apontar para o
        # MESMO objeto Artista (o artista não pertence a uma mídia só)
        self._artistas = []                # protegido

        self.__id_acervo = id(self)        # privado
        Acervo.total_acervos_criados += 1

    def buscar_artista(self, nome):
        nome_normalizado = nome.strip().lower()

        for artista in self._artistas:
            if artista.nome.strip().lower() == nome_normalizado:
                return artista

        return None

    def obter_ou_criar_artista(self, nome, pais_origem="Desconhecido"):
        artista_existente = self.buscar_artista(nome)
        if artista_existente is not None:
            # Já existe: reaproveita o mesmo objeto, sem alterar o país dele
            return artista_existente

        novo_artista = Artista(nome.strip(), pais_origem)
        self._artistas.append(novo_artista)
        return novo_artista

    def adicionar_midia(self, midia):
        self._midias.append(midia)
        print("Mídia registrada com sucesso!\n")

    def remover_midia(self, indice):
        # AGREGAÇÃO: o Artista NÃO é removido junto com a mídia; ele continua
        # no acervo. Já o RegistroCompra (COMPOSIÇÃO) deixa de existir com ela.
        midia_removida = self._midias.pop(indice)
        return midia_removida

    def editar_estado_midia(self, indice, novo_estado):
        midia = self._midias[indice]
        midia.estado_conservacao = novo_estado
        return midia

    def buscar_por_titulo(self, termo):
        termo_normalizado = termo.strip().lower()
        return [
            midia for midia in self._midias
            if termo_normalizado in midia.titulo.lower()
        ]

    def buscar_por_artista(self, termo):
        termo_normalizado = termo.strip().lower()
        return [
            midia for midia in self._midias
            if termo_normalizado in midia.artista.nome.lower()
        ]

    def buscar_por_formato(self, classe_formato):
        return [
            midia for midia in self._midias
            if isinstance(midia, classe_formato)
        ]

    def listar_artistas(self):
        if not self._artistas:
            return "Nenhum artista cadastrado."

        resultado = f"===== Artistas ({len(self._artistas)}) =====\n"
        for artista in self._artistas:
            qtd_midias = sum(1 for m in self._midias if m.artista == artista)
            resultado += f"- {artista.nome} (País: {artista.pais_origem} | Mídias no acervo: {qtd_midias})\n"
        return resultado

    def __str__(self):
        if not self._midias:
            return "O acervo está vazio."

        resultado = f"===== Acervo ({len(self._midias)} mídias) =====\n"
        for midia in self._midias:
            formato = type(midia).__name__
            resultado += f"- [{formato}] {midia.titulo} ({midia.artista.nome}) - {midia.data_lancamento} [{midia.estado_conservacao}]\n"
        return resultado