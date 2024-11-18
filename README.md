# Forest Fire AV2

Forest Fire AV2 se trata de um simulador [Python](https://www.python.org/) de incêndios florestais bidimensionais mais dinâmico, flexível e enriquecido sque implementações mais rudimentares do modelo. A liberdade na escolha de parâmetros permite ao usuário uma abordagem mais detalhada e lúdica da simulação. Os requisitos para o uso do modelo são apenas a [Livraria Original do Python](https://docs.python.org/3/library/) e o [FrameworK Mesa](https://mesa.readthedocs.io/stable/).

## Download e Instalação

Faça o download da versão mais recente por meio do [Repositório GitHub do Projeto](https://github.com/viniciusgma/AV2.git). Em seguida, por meio do terminal execute o comando `pip install -r requirements.txt` no diretório AV2-main. Após concluir o download dos requisitos, aplique o comando `python3 run.py`. 

## Utilização

Na janela do simulador o usuário tem acesso a vários parâmetros referentes aos diversos agentes do modelo, sendo eles agentes inertes (terra, ávore e água), agentes móveis (bombeiro, nuvem e pássaro) ou agentes virtuais (fogo). A intensidade dos parâmetros disponíveis para cada um dos agentes é amplamente flexível, gerando dinâmicas únicas de acordo com a configuração escolhida.

### Executar

dentro da pasta AV2 executar comando `mesa runserver`
### Set up

Depois de criar um env e executar `pip install -r requirements.txt` :

`pre-commit install`

`pre-commit run --all-files`

Ao executar pre-commit install, sempre, antes de um commit ser confirmado, serão executados os tests, um linter e um formatador, e o commit só passará se todos retornarem "passed".
