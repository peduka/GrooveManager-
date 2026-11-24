from models.acervo import Acervo
from models.vinil import Vinil
from models.cd import CD
from models.cassete import K7
from models.registro_compra import RegistroCompra
from models.buscador import BuscadorFichaTecnica
from views.dados_exemplo import carregar_dados_exemplo


class Menu:

    def __init__(self):
        self.acervo = Acervo()
        self._exemplos_carregados = False

    def iniciar(self):
        while True:
            print("\n--- GROOVEMANAGER ---")
            print("1 - Cadastrar Mídia")
            print("2 - Visualizar Acervo")
            print("3 - Ver Detalhes de uma Mídia")
            print("4 - Buscar Mídia")
            print("5 - Editar Estado de Conservação")
            print("6 - Remover Mídia")
            print("7 - Listar Artistas")
            print("8 - Pesquisar Ficha Técnica na Wikipedia")
            print("9 - Carregar Dados de Exemplo")
            print("10 - Sair")
            escolha = input("Escolha uma opção: ").strip()

            if escolha == "1":
                self.cadastrar_midia()
            elif escolha == "2":
                print(self.acervo)
            elif escolha == "3":
                self.ver_detalhes()
            elif escolha == "4":
                self.buscar_midia()
            elif escolha == "5":
                self.editar_midia()
            elif escolha == "6":
                self.remover_midia()
            elif escolha == "7":
                print("\n" + self.acervo.listar_artistas())
            elif escolha == "8":
                self.pesquisar_online()
            elif escolha == "9":
                self.carregar_exemplos()
            elif escolha == "10":
                print("Encerrando o sistema.")
                break
            else:
                print("Opção inválida.")

    def _selecionar_indice_midia(self, acao):
        if not self.acervo._midias:
            print("\nErro: O acervo está vazio.")
            return None

        print(f"\nEscolha uma mídia para {acao}:")
        for indice, midia in enumerate(self.acervo._midias):
            formato = type(midia).__name__
            print(f"{indice} - [{formato}] {midia.titulo} ({midia.artista.nome})")

        try:
            escolha = int(input("\nDigite o número da mídia: "))
            if 0 <= escolha < len(self.acervo._midias):
                return escolha
            print("Erro: Número fora da lista.")
            return None
        except ValueError:
            print("Erro: Digite apenas o número correspondente.")
            return None

    def cadastrar_midia(self):
        print("\n1 - Vinil\n2 - CD\n3 - Fita Cassete")
        opcao = input("Escolha o tipo de mídia: ").strip()

        tipos_por_numero = {"1": Vinil, "2": CD, "3": K7}

        if opcao not in tipos_por_numero:
            print("Opção inválida.")
            return

        classe_escolhida = tipos_por_numero[opcao]

        while True:
            titulo = input("Título do álbum: ").strip()
            if titulo:
                break
            print("Erro: o título não pode ficar vazio.")

        while True:
            entrada_ano = input("Ano de lançamento: ").strip()
            try:
                ano = int(entrada_ano)
                if 1877 <= ano <= 2100:
                    data_lancamento = str(ano)
                    break
                print("Erro: digite um ano válido (ex: 1975).")
            except ValueError:
                print("Erro: digite apenas números inteiros para o ano.")

        while True:
            nome_artista = input("Nome do Artista: ").strip()
            if nome_artista:
                break
            print("Erro: o nome do artista não pode ficar vazio.")

        # AGREGAÇÃO: reaproveita o Artista se ele já existir no acervo
        artista_obj = self.acervo.buscar_artista(nome_artista)
        if artista_obj is not None:
            print("Artista já cadastrado, reaproveitando.")
        else:
            pais = input("País de origem do artista: ").strip() or "Desconhecido"
            artista_obj = self.acervo.obter_ou_criar_artista(nome_artista, pais)

        print("\n1 - Lacrado\n2 - Excelente\n3 - Bom\n4 - Ruim")
        estados_por_numero = {"1": "Lacrado", "2": "Excelente", "3": "Bom", "4": "Ruim"}
        while True:
            opcao_estado = input("Escolha o estado de conservação: ").strip()
            if opcao_estado in estados_por_numero:
                estado_conservacao = estados_por_numero[opcao_estado]
                break
            print("Erro: escolha uma opção entre 1 e 4.")

        while True:
            entrada_valor = input("Valor pago (R$): ").strip()
            try:
                valor_float = float(entrada_valor.replace(",", "."))
                if valor_float < 0:
                    print("Erro: o valor não pode ser negativo.")
                    continue
                break
            except ValueError:
                print("Erro: digite um valor numérico válido (ex: 150.00).")

        data_prensagem = input("Data de prensagem: ").strip()
        local_prensagem = input("Local de prensagem: ").strip()

        try:
            registro = RegistroCompra(valor_float, data_prensagem, local_prensagem)
        except ValueError as erro:
            print(f"Erro ao criar registro de compra: {erro}")
            return

        nova_midia = classe_escolhida(titulo, data_lancamento, artista_obj, estado_conservacao, registro)
        self.acervo.adicionar_midia(nova_midia)

    def ver_detalhes(self):
        indice = self._selecionar_indice_midia("ver os detalhes")
        if indice is not None:
            self.acervo._midias[indice].exibir_ficha_tecnica()

    def buscar_midia(self):
        if not self.acervo._midias:
            print("\nErro: O acervo está vazio.")
            return

        print("\nBuscar por:")
        print("1 - Título")
        print("2 - Artista")
        print("3 - Formato (Vinil, CD ou K7)")
        opcao = input("Escolha o critério de busca: ").strip()

        if opcao == "1":
            termo = input("Digite o título (ou parte dele): ").strip()
            resultados = self.acervo.buscar_por_titulo(termo)
        elif opcao == "2":
            termo = input("Digite o nome do artista: ").strip()
            resultados = self.acervo.buscar_por_artista(termo)
        elif opcao == "3":
            print("1 - Vinil\n2 - CD\n3 - Fita Cassete (K7)")
            tipo = input("Escolha o formato: ").strip()
            mapa_formatos = {"1": Vinil, "2": CD, "3": K7}
            if tipo not in mapa_formatos:
                print("Formato inválido.")
                return
            resultados = self.acervo.buscar_por_formato(mapa_formatos[tipo])
        else:
            print("Opção de busca inválida.")
            return

        if not resultados:
            print("\nNenhuma mídia encontrada com esse critério.")
            return

        print(f"\n===== Resultados da Busca ({len(resultados)}) =====")
        for midia in resultados:
            formato = type(midia).__name__
            print(f"- [{formato}] {midia.titulo} ({midia.artista.nome}) - {midia.data_lancamento} [{midia.estado_conservacao}]")

    def editar_midia(self):
        indice = self._selecionar_indice_midia("editar o estado de conservação")
        if indice is None:
            return

        midia_atual = self.acervo._midias[indice]
        print(f"Estado atual de '{midia_atual.titulo}': {midia_atual.estado_conservacao}")
        print("\n1 - Lacrado\n2 - Excelente\n3 - Bom\n4 - Ruim")
        estados_por_numero = {"1": "Lacrado", "2": "Excelente", "3": "Bom", "4": "Ruim"}

        opcao_estado = input("Escolha o novo estado de conservação: ").strip()
        if opcao_estado not in estados_por_numero:
            print("Opção inválida. Alteração cancelada.")
            return

        novo_estado = estados_por_numero[opcao_estado]
        self.acervo.editar_estado_midia(indice, novo_estado)
        print(f"Estado de '{midia_atual.titulo}' atualizado para '{novo_estado}' com sucesso!")

    def remover_midia(self):
        indice = self._selecionar_indice_midia("remover")
        if indice is None:
            return

        midia = self.acervo._midias[indice]
        confirmacao = input(f"Tem certeza que deseja remover '{midia.titulo}'? (s/n): ").strip().lower()
        if confirmacao == "s":
            removida = self.acervo.remover_midia(indice)
            print(f"Mídia '{removida.titulo}' removida do acervo.")
        else:
            print("Remoção cancelada.")

    def pesquisar_online(self):
        indice = self._selecionar_indice_midia("pesquisar na Wikipedia")
        if indice is not None:
            midia_selecionada = self.acervo._midias[indice]
            buscador = BuscadorFichaTecnica()
            buscador.pesquisar_wikipedia(midia_selecionada)

    def carregar_exemplos(self):
        if self._exemplos_carregados:
            print("\nDados de exemplo já carregados.")
            return

        carregar_dados_exemplo(self.acervo)
        self._exemplos_carregados = True
        print("\nDados de exemplo carregados com sucesso!")