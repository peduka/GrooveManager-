# GrooveManager

Sistema desktop em Python com interface gráfica (`tkinter` / `ttk`) para catalogar
acervos de mídias físicas (discos de vinil, CDs e fitas cassete). Projeto da
disciplina de Orientação a Objetos (UnB FGA).

> Status: Desk App IV (versão final). Interface gráfica desktop com múltiplas
> janelas, botões e estilos personalizados (tema escuro *Dark Vinyl Studio*) e
> persistência em banco de dados SQLite (`groovemanager.db`), criado
> automaticamente na primeira execução.

## Funcionalidades

- **Interface gráfica completa:** janela principal com tabela estilizada
  (`ttk.Treeview`), barra de filtros em tempo real, rodapé de status e janelas
  modais (`Toplevel`) para cada operação
- **Botões e estilos personalizados:** tema escuro customizado via `ttk.Style`
  e botões com paleta semântica e efeito *hover* (`BotaoEstilizado`)
- Cadastrar mídias (vinil, CD ou fita cassete) em formulário gráfico com
  validação de título, ano, artista, estado de conservação e valor pago
- Registro de compra de cada mídia: valor, data e local de prensagem
- **Agregação em tempo real:** ao digitar o nome de um artista já cadastrado,
  a interface identifica automaticamente, reaproveita o registro e bloqueia o
  campo de país de origem
- Exibir ficha técnica completa de uma mídia em janela dedicada (duplo clique
  na tabela ou botão **Ver Ficha Técnica**)
- Buscar e filtrar mídias por título, artista ou formato
- Editar o estado de conservação em janela modal
- Remover mídia com caixa de confirmação
- Listar artistas em janela dedicada (com país e quantidade de mídias no acervo)
- Pesquisar a mídia na Wikipedia diretamente pelo navegador
- Carregar dados de exemplo sem duplicar registros já existentes
- **Persistência em banco de dados:** os dados continuam salvos ao fechar e
  abrir o programa
- Inspecionar o conteúdo bruto das tabelas do SQLite em abas diretamente pela
  interface

## Banco de dados

SQLite (biblioteca `sqlite3` do próprio Python, sem instalar nada). As operações
de banco acontecem no `RepositorioSQLite`:

| Ação na interface | Operação no banco |
|---|---|
| Abrir o programa | `SELECT` (carrega artistas e mídias salvos) |
| Cadastrar mídia / artista | `INSERT` |
| Editar estado de conservação | `UPDATE` |
| Remover mídia | `DELETE` |
| Botão **Banco SQLite** | `SELECT` em todas as tabelas (exibidas em abas) |

As relações de POO aparecem no esquema:

- **Agregação:** `artistas` existe independente. Remover uma mídia não remove o
  artista.
- **Composição:** `registros_compra` depende de `midias`, com `ON DELETE CASCADE`.
  Remover a mídia remove o registro de compra junto.

```mermaid
erDiagram
    ARTISTAS ||--o{ MIDIAS : "agregacao"
    MIDIAS ||--|| REGISTROS_COMPRA : "composicao (ON DELETE CASCADE)"
    ARTISTAS {
        INTEGER id PK
        TEXT nome UK
        TEXT pais_origem
    }
    MIDIAS {
        INTEGER id PK
        TEXT formato
        TEXT titulo
        TEXT data_lancamento
        TEXT estado_conservacao
        INTEGER artista_id FK
    }
    REGISTROS_COMPRA {
        INTEGER id PK
        INTEGER midia_id FK
        REAL valor
        TEXT data_prensagem
        TEXT local_prensagem
    }
```

## Conceitos de POO aplicados

- **Herança e polimorfismo:** `Vinil`, `CD` e `K7` herdam da classe abstrata
  `Midia` e implementam `exibir_ficha_tecnica()` cada um do seu jeito; na
  interface gráfica, `BotaoEstilizado` herda de `tk.Button`
- **Composição:** cada mídia tem um `RegistroCompra` que só existe atrelado a ela
- **Agregação:** o `Artista` existe de forma independente e pode estar ligado a
  várias mídias; o `Acervo` também agrega mídias e artistas
- **Associação:** o `Acervo` usa um `RepositorioSQLite` para persistir os dados,
  e `InterfaceGrafica` recebe o `Acervo` para orquestrar a tela
- **Dependência:** `BuscadorFichaTecnica` e `RepositorioSQLite` recebem ou criam
  mídias apenas para usá-las
- **Encapsulamento:** atributos privados, protegidos e públicos com `@property`

## Como executar

Na pasta raiz do projeto:

    python main.py

O arquivo `groovemanager.db` é criado ao lado do `main.py`. Para começar do zero,
feche o programa e apague esse arquivo.

## Estrutura

    main.py
    models/   (Midia, Vinil, CD, K7, Artista, RegistroCompra, Acervo,
               BuscadorFichaTecnica, RepositorioSQLite)
    views/    (InterfaceGrafica, BotaoEstilizado, Menu, dados_exemplo)
    extras/   (versão 2 da Midia, usada só para comparação)

## Diagrama UML

![Diagrama UML](GrooveManager_UML.png)