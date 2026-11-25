from pathlib import Path

from models.acervo import Acervo
from models.repositorio import ErroRepositorio, RepositorioSQLite
from views.interface_grafica import InterfaceGrafica

# O arquivo do banco fica ao lado do main.py e é criado sozinho na primeira vez
CAMINHO_BANCO = Path(__file__).resolve().parent / "groovemanager.db"


def main():
    try:
        repositorio = RepositorioSQLite(CAMINHO_BANCO)
        acervo = Acervo(repositorio)
    except ErroRepositorio as erro:
        print(f"Não foi possível abrir o banco de dados: {erro}")
        return

    try:
        InterfaceGrafica(acervo).iniciar()
    finally:
        repositorio.fechar()


if __name__ == "__main__":
    main()