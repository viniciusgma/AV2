# Forest Fire AV2

Forest Fire AV2 é um simulador [Python](https://www.python.org/) de incêndios florestais em um ambiente bidimensional, sendo mais dinâmico, flexível e enriquecido que implementações mais rudimentares do modelo. A liberdade na escolha de parâmetros permite ao usuário uma abordagem mais detalhada e lúdica da simulação, permitindo uma análise visual em tempo real do comportamento do fogo. Os requisitos para o uso do modelo são apenas a [Livraria Original do Python](https://docs.python.org/3/library/) e o [Framework Mesa](https://mesa.readthedocs.io/stable/).

## Download e Instalação

Faça o download da versão mais recente por meio do [Repositório GitHub do Projeto](https://github.com/viniciusgma/AV2.git). Em seguida, por meio do terminal execute o comando `pip install -r requirements.txt` no diretório AV2-main. Após concluir o download dos requisitos, aplique o comando `python3 run.py`.

## Utilização

Na janela do simulador o usuário tem acesso a vários parâmetros referentes aos diversos agentes do modelo, sendo eles agentes inertes (terra, árvore e água), agentes móveis (bombeiro, nuvem e pássaro) ou agentes virtuais (fogo). Todos os parâmetros são ajustáveis, e as variadas configurações geram dinâmicas particulares.

[Exposição do Modelo](https://github-production-user-asset-6210df.s3.amazonaws.com/167988419/387339222-278e0798-58af-403e-91d8-7b2e26ec37fc.webm?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20241118%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241118T185018Z&X-Amz-Expires=300&X-Amz-Signature=542084921f9b8aed398c9d33d3b753de839fec072978017c1e837443dcd87390&X-Amz-SignedHeaders=host)

### Executar

dentro da pasta AV2 executar comando `mesa runserver`
### Set up

Depois de criar um env e executar `pip install -r requirements.txt` :

`pre-commit install`

`pre-commit run --all-files`

Ao executar pre-commit install, sempre, antes de um commit ser confirmado, serão executados os tests, um linter e um formatador, e o commit só passará se todos retornarem "passed".
