import webbrowser
import urllib.parse


class BuscadorFichaTecnica:

    def pesquisar_wikipedia(self, midia):
        termo_busca = f"{midia.artista.nome} {midia.titulo} album"
        termo_formatado = urllib.parse.quote(termo_busca)

        url = f"https://pt.wikipedia.org/wiki/Special:Search?search={termo_formatado}"

        print(f"\n[Buscador] Abrindo a Wikipedia para: {midia.titulo}...")
        webbrowser.open(url)