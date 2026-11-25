import functools
import sqlite3

from models.artista import Artista
from models.registro_compra import RegistroCompra
from models.vinil import Vinil
from models.cd import CD
from models.cassete import K7


class ErroRepositorio(Exception):
    """Erro ao acessar o banco de dados."""


def _traduzir_erros(funcao):
    # Converte qualquer erro do SQLite em ErroRepositorio, para o resto do
    # programa não precisar conhecer o sqlite3.
    @functools.wraps(funcao)
    def interna(*args, **kwargs):
        try:
            return funcao(*args, **kwargs)
        except sqlite3.Error as erro:
            raise ErroRepositorio(str(erro)) from erro
    return interna


class RepositorioSQLite:
    """Guarda e recupera artistas e mídias em um banco SQLite.

    Como o banco reflete as relações de POO:
    - AGREGAÇÃO: um artista (tabela artistas) existe independente das mídias.
      Apagar uma mídia NÃO apaga o artista.
    - COMPOSIÇÃO: o registro de compra (tabela registros_compra) só existe
      ligado a uma mídia. Apagar a mídia apaga o registro (ON DELETE CASCADE).
    """

    FORMATOS = {"Vinil": Vinil, "CD": CD, "K7": K7}      # público
    TABELAS = ("artistas", "midias", "registros_compra")  # público

    def __init__(self, caminho_banco):
        self.__caminho = str(caminho_banco)   # privado
        self._conexao = None                  # protegido
        self._ids_artistas = {}               # protegido: objeto Artista -> id no banco
        self._ids_midias = {}                 # protegido: objeto Midia -> id no banco
        self._conectar()
        self._criar_tabelas()

    @_traduzir_erros
    def _conectar(self):
        self._conexao = sqlite3.connect(self.__caminho)
        self._conexao.row_factory = sqlite3.Row
        # Sem isso o SQLite ignora as chaves estrangeiras (e o ON DELETE CASCADE)
        self._conexao.execute("PRAGMA foreign_keys = ON")

    @_traduzir_erros
    def _criar_tabelas(self):
        with self._conexao:
            self._conexao.execute("""
                CREATE TABLE IF NOT EXISTS artistas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    pais_origem TEXT NOT NULL
                )
            """)
            self._conexao.execute("""
                CREATE TABLE IF NOT EXISTS midias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    formato TEXT NOT NULL CHECK (formato IN ('Vinil', 'CD', 'K7')),
                    titulo TEXT NOT NULL,
                    data_lancamento TEXT NOT NULL,
                    estado_conservacao TEXT NOT NULL,
                    artista_id INTEGER NOT NULL REFERENCES artistas(id)
                )
            """)
            self._conexao.execute("""
                CREATE TABLE IF NOT EXISTS registros_compra (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    midia_id INTEGER NOT NULL UNIQUE
                        REFERENCES midias(id) ON DELETE CASCADE,
                    valor REAL NOT NULL CHECK (valor >= 0),
                    data_prensagem TEXT NOT NULL,
                    local_prensagem TEXT NOT NULL
                )
            """)

    def _id_da_midia(self, midia):
        if midia not in self._ids_midias:
            raise ErroRepositorio("Esta mídia não está registrada no banco de dados.")
        return self._ids_midias[midia]

    # ---------- SELECT ----------
    @_traduzir_erros
    def carregar_tudo(self):
        """Lê o banco e devolve (lista de artistas, lista de mídias) como objetos."""
        artistas = []
        artistas_por_id = {}
        for linha in self._conexao.execute(
                "SELECT id, nome, pais_origem FROM artistas ORDER BY id"):
            artista = Artista(linha["nome"], linha["pais_origem"])
            self._ids_artistas[artista] = linha["id"]
            artistas_por_id[linha["id"]] = artista
            artistas.append(artista)

        midias = []
        consulta = """
            SELECT m.id, m.formato, m.titulo, m.data_lancamento,
                   m.estado_conservacao, m.artista_id,
                   r.valor, r.data_prensagem, r.local_prensagem
            FROM midias m
            JOIN registros_compra r ON r.midia_id = m.id
            ORDER BY m.id
        """
        for linha in self._conexao.execute(consulta):
            registro = RegistroCompra(linha["valor"], linha["data_prensagem"],
                                      linha["local_prensagem"])
            classe = self.FORMATOS[linha["formato"]]
            midia = classe(linha["titulo"], linha["data_lancamento"],
                           artistas_por_id[linha["artista_id"]],
                           linha["estado_conservacao"], registro)
            self._ids_midias[midia] = linha["id"]
            midias.append(midia)

        return artistas, midias

    @_traduzir_erros
    def consultar_tabelas(self):
        """Devolve {tabela: (colunas, linhas)} com o conteúdo bruto do banco."""
        resultado = {}
        for tabela in self.TABELAS:
            cursor = self._conexao.execute(f"SELECT * FROM {tabela} ORDER BY id")
            colunas = [coluna[0] for coluna in cursor.description]
            resultado[tabela] = (colunas, [tuple(linha) for linha in cursor.fetchall()])
        return resultado

    # ---------- INSERT ----------
    @_traduzir_erros
    def inserir_artista(self, artista):
        if artista in self._ids_artistas:
            return
        with self._conexao:
            cursor = self._conexao.execute(
                "INSERT INTO artistas (nome, pais_origem) VALUES (?, ?)",
                (artista.nome, artista.pais_origem))
        self._ids_artistas[artista] = cursor.lastrowid

    @_traduzir_erros
    def inserir_midia(self, midia):
        self.inserir_artista(midia.artista)   # garante que o artista já existe no banco
        registro = midia.registro_compra
        with self._conexao:   # as duas inserções valem juntas ou não valem
            cursor = self._conexao.execute(
                "INSERT INTO midias (formato, titulo, data_lancamento, "
                "estado_conservacao, artista_id) VALUES (?, ?, ?, ?, ?)",
                (type(midia).__name__, midia.titulo, midia.data_lancamento,
                 midia.estado_conservacao, self._ids_artistas[midia.artista]))
            id_midia = cursor.lastrowid
            self._conexao.execute(
                "INSERT INTO registros_compra (midia_id, valor, data_prensagem, "
                "local_prensagem) VALUES (?, ?, ?, ?)",
                (id_midia, registro.valor, registro.data_prensagem,
                 registro.local_prensagem))
        self._ids_midias[midia] = id_midia

    # ---------- UPDATE ----------
    @_traduzir_erros
    def atualizar_estado(self, midia):
        id_midia = self._id_da_midia(midia)
        with self._conexao:
            self._conexao.execute(
                "UPDATE midias SET estado_conservacao = ? WHERE id = ?",
                (midia.estado_conservacao, id_midia))

    # ---------- DELETE ----------
    @_traduzir_erros
    def remover_midia(self, midia):
        id_midia = self._id_da_midia(midia)
        with self._conexao:
            # O registro de compra é apagado junto (ON DELETE CASCADE).
            # O artista NÃO é apagado.
            self._conexao.execute("DELETE FROM midias WHERE id = ?", (id_midia,))
        del self._ids_midias[midia]

    def fechar(self):
        if self._conexao is not None:
            self._conexao.close()
            self._conexao = None