from models.artista import Artista


class Acervo:

    total_acervos_criados = 0 # público

    def __init__(self):
        self._midias = []                  # protegido

        # RELAÇÃO DE AGREGAÇÃO: o Acervo guarda os Artistas de forma
        # independente das mídias. Várias mídias podem apontar para o
        # MESMO objeto Artista (o artista não pertence a uma mídia só)
        self._artistas = []                # protegido

        self.__id_acervo = id(self)        # privado
        Acervo.total_acervos_criados += 1

    def obter_ou_criar_artista(self, nome):
        nome = nome.strip()
        nome_normalizado = nome.lower()

        for artista in self._artistas:
            if artista.nome.strip().lower() == nome_normalizado:
                return artista

        novo_artista = Artista(nome)
        self._artistas.append(novo_artista)
        return novo_artista

    def adicionar_midia(self, midia):
        self._midias.append(midia)
        print("Mídia registrada com sucesso!\n")

    def __str__(self):
        if not self._midias:
            return "O acervo está vazio."

        resultado = f"===== Acervo ({len(self._midias)} mídias) =====\n"
        for midia in self._midias:
            resultado += f"- {midia.titulo} ({midia.artista.nome}) - {midia.data_lancamento}\n"
        return resultado