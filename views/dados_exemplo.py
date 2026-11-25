# Apenas para demonstração. Com o banco de dados, não duplica as mídias que
# já estão no acervo (pode ser escolhido várias vezes, inclusive em dias
# diferentes, sem repetir nada).

from models.vinil import Vinil
from models.cd import CD
from models.cassete import K7
from models.registro_compra import RegistroCompra


def _ja_existe(acervo, classe, titulo, nome_artista):
    for midia in acervo.buscar_por_titulo(titulo):
        if (type(midia) is classe
                and midia.titulo.lower() == titulo.lower()
                and midia.artista.nome.lower() == nome_artista.lower()):
            return True
    return False


def carregar_dados_exemplo(acervo):
    """Cadastra as mídias de exemplo que ainda não existem. Devolve quantas foram criadas."""
    # (formato, título, ano, artista, país, estado, valor, data de prensagem, local de prensagem)
    exemplos = [
        (Vinil, "Doolittle", "1989", "Pixies", "EUA", "Excelente", 180.00, "22/08/1990", "Inglaterra"),
        (CD, "Surfer Rosa", "1988", "Pixies", "EUA", "Bom", 100.00, "30/10/2001", "EUA"),
        (Vinil, "Tim Maia", "1970", "Tim Maia", "Brasil", "Bom", 250.00, "10/11/1970", "Brasil"),
        (K7, "The Dark Side of the Moon", "1973", "Pink Floyd", "Inglaterra", "Excelente", 60.00, "01/03/1973", "Inglaterra"),
    ]

    adicionadas = 0
    for classe, titulo, ano, nome_artista, pais, estado, valor, data_prensagem, local in exemplos:
        if _ja_existe(acervo, classe, titulo, nome_artista):
            continue

        # O mesmo Artista é reaproveitado (os dois discos dos Pixies apontam para o mesmo objeto)
        artista = acervo.obter_ou_criar_artista(nome_artista, pais)
        registro = RegistroCompra(valor, data_prensagem, local)
        midia = classe(titulo, ano, artista, estado, registro)
        acervo.adicionar_midia(midia)
        adicionadas += 1

    return adicionadas