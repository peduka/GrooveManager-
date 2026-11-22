# GrooveManager

Sistema em Python, executado no terminal, para catalogar acervos de mídias físicas
(discos de vinil, CDs e fitas cassete). Projeto da disciplina de Orientação a
Objetos (UnB FGA).

## Funcionalidades

- Cadastrar mídias (vinil, CD ou fita cassete) com artista, ano, estado de
  conservação e registro de compra
- Visualizar o acervo
- Ver a ficha técnica completa de uma mídia
- Pesquisar a mídia na Wikipedia

## Conceitos de POO aplicados

- **Herança e polimorfismo:** Vinil, CD e K7 herdam da classe abstrata Midia e
  implementam `exibir_ficha_tecnica()` cada um do seu jeito
- **Composição:** cada mídia tem um RegistroCompra que só existe atrelado a ela
- **Agregação:** o Artista existe de forma independente e pode estar ligado a
  várias mídias
- **Dependência:** BuscadorFichaTecnica recebe a mídia apenas como parâmetro
- **Encapsulamento:** atributos privados, protegidos e públicos com @property

## Como executar

Na pasta raiz do projeto:

    python main.py

## Estrutura

    main.py
    models/   (Midia, Vinil, CD, K7, Artista, RegistroCompra, Acervo, BuscadorFichaTecnica)
    views/    (Menu)
    extras/   (versão 2 da Midia, usada só para comparação)

## Diagrama UML

Em breve.