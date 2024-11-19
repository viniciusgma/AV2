# Forest Fire AV2 - Usage

## Sumário 
Essa é uma versão expandida do modelo de Forest Fire, com algumas alterações nas interações entre as árvores e seus estados com a adição de cinco agentes, sendo eles terra, água, nuvem, bombeiro e pássaro.
## Resumo dos agentes
### Árvore
Recebeu mudanças em relação ao modelo base, apresentando boa condição quando com mais de 70% da vida, em chamas no intervalo de 30% a 70% da vida e queimada quando com menos de 30% de vida. A taxa de queima é facultativa, de modo que quando em boa condição apresenta redução de metade dessa taxa para cada vizinho em chamas (alastramento do fogo), e quando em estado de queima sofre redução da taxa integral. Quando queimando, a árvore não é afetada pelo alastramento do fogo.
### Terra
Agente passivo sem interações com qualquer outro agente, podendo ser transformado em uma árvore pelo pássaro.
### Rio
Agente inerte que constantemente regenera em 30% a vida de árvores próximas cuja condição é inferior a 70%.
###Nuvem
A Nuvem é um agente que pode surgir em qualquer ponto do grid, composto por quatro células posicionadas nos cantos de um espaço 3x3. Suas características e interações são descritas abaixo:
- Chuva e Raios  
  A nuvem pode causar chuva ou raios, com probabilidades definidas pelos sliders do experimento.
  - Chuva:
    - Aumenta a vida da árvore em +0.1 se ela estiver perdendo a vida.
    - Apaga o fogo da árvore se a intensidade da chuva for maior que a do fogo.  
      - Ambos os processos reduzem a vida da nuvem em -0.1.
    - Substitui árvores queimadas por terra.
  - Raios: WIP


