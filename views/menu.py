from models.acervo import Acervo
from models.vinil import Vinil
from models.cd import CD
from models.cassete import K7
from models.registro_compra import RegistroCompra
from models.buscador import BuscadorFichaTecnica


class Menu:

    def __init__(self):
        self.acervo = Acervo()

    def iniciar(self):
        while True:
            print("\n--- GROOVEMANAGER ---")
            print("1 - Cadastrar Mídia")
            print("2 - Visualizar Acervo")
            print("3 - Pesquisar Ficha Técnica na Wikipedia")
            print("4 - Ver Detalhes de uma Mídia")
            print("5 - Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                self.cadastrar_midia()
            elif escolha == "2":
                print(self.acervo)
            elif escolha == "3":
                self.pesquisar_online()
            elif escolha == "4":
                self.ver_detalhes()
            elif escolha == "5":
                print("Encerrando o sistema.")
                break
            else:
                print("Opção inválida.")

    def cadastrar_midia(self):
        print("\n1 - Vinil\n2 - CD\n3 - Fita Cassete")
        opcao = input("Escolha o tipo de mídia: ")

        tipos_por_numero = {"1": Vinil, "2": CD, "3": K7}

        if opcao not in tipos_por_numero:
            print("Opção inválida.")
            return

        classe_escolhida = tipos_por_numero[opcao]

        titulo = input("Título do álbum: ")

        while True:
            data_lancamento = input("Ano de lançamento: ")
            if data_lancamento.isdigit():
                break
            print("Erro: digite apenas números.")

        while True:
            nome_artista = input("Nome do Artista: ").strip()
            if nome_artista:
                break
            print("Erro: o nome do artista não pode ficar vazio.")

        # AGREGAÇÃO: reaproveita o Artista se ele já existir no acervo
        artista_obj = self.acervo.obter_ou_criar_artista(nome_artista)
        print("\n1 - Lacrado\n2 - Excelente\n3 - Bom\n4 - Ruim")
        opcao_estado = input("Escolha o estado de conservação: ")

        estados_por_numero = {"1": "Lacrado", "2": "Excelente", "3": "Bom", "4": "Ruim"}
        estado_conservacao = estados_por_numero.get(opcao_estado, "Não avaliado")

        valor = input("Valor pago (R$): ")
        data_prensagem = input("Data de prensagem: ")
        local_prensagem = input("Local de prensagem: ")
        registro = RegistroCompra(valor, data_prensagem, local_prensagem)

        nova_midia = classe_escolhida(titulo, data_lancamento, artista_obj, estado_conservacao, registro)
        self.acervo.adicionar_midia(nova_midia)

    def pesquisar_online(self):
        if not self.acervo._midias:
            print("\nErro: O acervo está vazio. Cadastre um disco primeiro!")
            return

        print("\nEscolha um disco registrado para pesquisar:")
        for indice, midia in enumerate(self.acervo._midias):
            print(f"{indice} - {midia.titulo} ({midia.artista.nome})")

        try:
            escolha = int(input("\nDigite o número do disco: "))

            if 0 <= escolha < len(self.acervo._midias):
                midia_selecionada = self.acervo._midias[escolha]
                buscador = BuscadorFichaTecnica()
                buscador.pesquisar_wikipedia(midia_selecionada)
            else:
                print("Erro: Número fora da lista.")
        except ValueError:
            print("Erro: Digite apenas o número correspondente.")

    def ver_detalhes(self):
        if not self.acervo._midias:
            print("\nErro: O acervo está vazio.")
            return

        print("\nEscolha uma mídia para ver os detalhes:")
        for indice, midia in enumerate(self.acervo._midias):
            print(f"{indice} - {midia.titulo} ({midia.artista.nome})")

        try:
            escolha = int(input("\nDigite o número da mídia: "))
            if 0 <= escolha < len(self.acervo._midias):
                self.acervo._midias[escolha].exibir_ficha_tecnica()
            else:
                print("Erro: Número fora da lista.")
        except ValueError:
            print("Erro: Digite apenas o número correspondente.")