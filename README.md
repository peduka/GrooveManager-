# GrooveManager

Sistema em Python, executado no terminal, para catalogar acervos de mÃ­dias fÃ­sicas
(discos de vinil, CDs e fitas cassete). Projeto da disciplina de OrientaÃ§Ã£o a
Objetos (UnB FGA).

## Funcionalidades

- Cadastrar mÃ­dias (vinil, CD ou fita cassete) com artista, ano, estado de
  conservaÃ§Ã£o e registro de compra
- Visualizar o acervo
- Ver a ficha tÃ©cnica completa de uma mÃ­dia
- Pesquisar a mÃ­dia na Wikipedia

## Conceitos de POO aplicados

- **HeranÃ§a e polimorfismo:** Vinil, CD e K7 herdam da classe abstrata Midia e
  implementam `exibir_ficha_tecnica()` cada um do seu jeito
- **ComposiÃ§Ã£o:** cada mÃ­dia tem um RegistroCompra que sÃ³ existe atrelado a ela
- **AgregaÃ§Ã£o:** o Artista existe de forma independente e pode estar ligado a
  vÃ¡rias mÃ­dias
- **DependÃªncia:** BuscadorFichaTecnica recebe a mÃ­dia apenas como parÃ¢metro
- **Encapsulamento:** atributos privados, protegidos e pÃºblicos com @property

## Como executar

Na pasta raiz do projeto:

    python main.py

## Estrutura

    main.py
    models/   (Midia, Vinil, CD, K7, Artista, RegistroCompra, Acervo, BuscadorFichaTecnica)
    views/    (Menu)
    extras/   (versÃ£o 2 da Midia, usada sÃ³ para comparaÃ§Ã£o)

## Diagrama UML

![Diagrama UML](GrooveManager_UML.png)
