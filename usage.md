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
### Nuvem
A Nuvem é um agente que pode surgir em qualquer ponto do grid, composto por quatro células posicionadas nos cantos de um espaço 3x3. Suas características e interações são descritas abaixo:
- Chuva e Raios  
  A nuvem pode causar chuva ou raios, com probabilidades definidas pelos sliders do experimento.
  - Chuva:
    - Aumenta a vida da árvore em +0.1 se ela estiver perdendo a vida.
    - Apaga o fogo da árvore se a intensidade da chuva for maior que a do fogo.  
      - Ambos os processos reduzem a vida da nuvem em -0.1.
    - Substitui árvores queimadas por terra.
  - Raios: faz com a arvore pegue fogo.
 ### Bombeiro
Agente dinâmico em constante movimento, movendo-se até o fogo mais próximo. Caso não haja fogo, seu movimento é aleatório. Quando uma árvore  próxima possui entre 30% e 70% de vida ele recupera 0.3 da condição da árvore ao passo que perde 0.1 da própria vida.
### Pássaro
Agente dinâmico em constante movimento, movendo-se em direção ao bloco de terra mais próximo. Caso não haja terra, seu movimento é aleatório. O agente atua semeando árvores em blocos de terra ociosos, com perda de 0.1 de vitalidade para cada unidade de terra semeada. O agente sofre 0.8 de dano ao passar pelo fogo.

## Sliders
São os valores que podem ser manipulados pelo usuário antes que do começo da simulação mudando o estado e interações dentro do grid.

### Sliders de estado inicial
Definem variáveis relacionadas ao grid antes do começo da simulação.
- **Densidade de Árvores**: define quanto da área total do grid será preenchida de forma a completar a mesma proporção dada.
- **Qtd de rios**: define quantos rios, faixas de água, terá no total da simulação.
- **Focos de incêndio**: determina a quantidade de árvores que estão pegando fogo para começar a simulação, que são escolhidas aleatoriamente.

### Sliders da nuvem
Definem variáveis relacionadas a nuvem e suas interações durante os passos.
- **Qtd de nuvem**: define quantidade de nuvens que constantemente estará na simulação
- **Probabilidade de Raio**: define a probabilidade de um raio acontecer na posição da nuvem.
- **Probabilidadede chuva**: define  a probabilidade da chuva  acontecer na posição da nuvem.
- **intesidade da chuva**: defiena a intensidade de todas as chuvas do modelo.
  
### Sliders dos Bombeiros
Definem variáveis relacionadas aos bombeiros.
- **Vida do Bombeiros**: define a vida inicial do bombeiro ao spawnar.
- **Intervalo Spawn Bombeiro**: define a quantidade de passos da simulação entre os spawns de bombeiros.
- **Qtd Inicial de Bombeiros**: define quantos bombeiros vão estar no começo da simulação.
- **Qtd de novos Bombeiros**: define quantos bonbeiros vão spawar a cada intevalo de spawn.
  
### Slider do fogo
Definem variáveis relacionadas ao fogo e suas interações durante os passos.
- **Taxa de queima**:
- **Taxa Propagação do fogo entre Árvores**:
- **Vida das Árvores**:
- **Intensidade do Fogo**:

### Sliders dos passaros
Definem variáveis relacionadas aos passaros.
- **Qtd de Pássaro**: define quantos passaros vão estar no começo da simulação.
- **Tempo de Spawn Pássaro**: define a quantidade de passos da simulação entre os spawns de passaros.
- **Vida Pássaro**: define a vida inicial do passaro ao spawnar.
- **Qtd de Novos Pássaros**: define quantos passaros vão spawar a cada tempo de spawn.

