import mesa
import random
from collections import deque


class Terra(mesa.Agent):
    def __init__(self, pos, model):
        """ 
        Cria uma célula de terra. O seu estado pode ser modificado
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = None


class TreeCell(mesa.Agent):
    """
    Representa uma árvore que pode estar em diferentes estados, como saudável, pegando fogo ou queimada.

    Atributos:
        pos: Posições da árvore no modelo.
        condition: Pode ser 'Fine' (saudável), 'On Fire' (pegando fogo) ou 'Burned Out' (queimada).
        unique_id: Identificador único da árvore, baseado em suas coordenadas.

    O objetivo é simular o crescimento e a propagação do fogo entre as árvores, afetando o estado delas.
    """

    def __init__(self, pos, model):
        """
        Cria uma nova árvora.

        Args:
            pos: A posição da árvore no modelo.
            model: Referência ao modelo onde o agente está inserido.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = 1

    def step(self):
        """
        Se a árvore está pegando fogo, ela espalha fogo para as árvores mais próximas.
        """
        if 0 < self.condition < 0.7:
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.condition:
                    neighbor.condition -= 0.1
                    if 0 < neighbor.condition < 0.7:
                        self.condition -= 0.1


class Fireman(mesa.Agent):
    """
    Classe para o bombeiro, que agora usa BFS para encontrar o fogo mais próximo.
    """

    def __init__(self, pos, model):
        """
        Cria um novo bombeiro.

        Args:
            pos: Coordenadas iniciais do bombeiro no grid.
            model: Referência ao modelo.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = 200  # Vida do bombeiro

    def bfs_to_fire(self):
        """
        Executa uma busca em largura (BFS) para encontrar a célula de árvore mais próxima
        que está pegando fogo (condition < 0.7).
        """
        queue = deque([self.pos])
        visited = {self.pos}

        while queue:
            current_pos = queue.popleft()

            # Verifica os vizinhos
            for neighbor in self.model.grid.get_neighbors(
                current_pos, moore=True, include_center=False
            ):
                if neighbor.pos not in visited:
                    visited.add(neighbor.pos)
                    queue.append(neighbor.pos)

                    # Se a célula do vizinho for uma árvore em fogo
                    if isinstance(neighbor, TreeCell) and 0 < neighbor.condition < 0.7:
                        return (
                            neighbor.pos
                        )  # Retorna a posição da árvore em fogo mais próxima
        return None  # Nenhum fogo encontrado

    def step(self):
        """
        Ação do bombeiro em cada passo: usa a BFS para encontrar o fogo mais próximo e se move na direção dele.
        """

        # Tenta encontrar a posição de uma árvore em fogo
        target_pos = self.bfs_to_fire()

        # Se houver um alvo em fogo, move-se na direção dele
        if target_pos:
            x, y = self.pos
            tx, ty = target_pos

            # Movimenta-se em direção ao fogo
            new_pos = (
                x + (1 if tx > x else -1 if tx < x else 0),
                y + (1 if ty > y else -1 if ty < y else 0),
            )

            self.model.grid.move_agent(self, new_pos)

            # Apaga o fogo e reduz a vida do bombeiro
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if isinstance(neighbor, TreeCell) and neighbor.condition < 0.7:
                    neighbor.condition += 0.2  # Apaga um pouco o fogo
                    self.condition -= 0.1  # Bombeiro perde vida

        # Se não há fogo encontrado, move-se aleatoriamente
        else:
            x, y = self.pos
            new_pos = (x + random.randint(-1, 1), y + random.randint(-1, 1))
            self.model.grid.move_agent(self, new_pos)

        # Remove se morreu
        if self.condition <= 0:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)


class River(mesa.Agent):
    """
    Representa um rio.
    Adiciona-se vida as árvoes que estão até trés grids de distancia do rio.
    """

    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = 1.5  # nerfado de 2 -> 1.5

    def step(self):
        dq = deque()
        dq.append(self)
        visited = []
        if self.condition > 0:
            while len(visited) <= 16:
                current = dq.popleft()
                dq.extend(current.model.grid.iter_neighbors(current.pos, True))
                if current not in visited:
                    visited.append(current)
                if current not in visited:
                    visited.append(current)
                if isinstance(current, TreeCell) and current.condition < 0.7:
                    current.condition += 0.3
                elif isinstance(current, River) and current.condition < 0.7:
                    current.condition += 0.05


class cloud(mesa.Agent):
    """
    A nuvem possui duas ações possiveis:

    lightning - joga um raio exatamente na árvore da mesma célula, fazendo ela pegar fogo
    rain - faz chover em um raio específico, aumentando a vida de todas
    e fazendo o fogo parar se existir.

    """

    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = 2000

    def step(self):
        """

        Joga um raio em um raio de 1 grid. 5% de chance de ocorrer

        """
        num = random.randint(1, 20)
        if num <= 5:
            if self.condition > 0:
                for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                    if isinstance(neighbor, TreeCell):
                        neighbor.condition = 0.699  # coloca arvore em fogo

        """

        Raio da chuva de 5 grids.

        """
        if self.condition > 0:
            radius = self.model.grid.get_neighbors(self.pos, moore=True, radius=2)
            for coisa in radius:
                if isinstance(coisa, TreeCell):
                    coisa.condition += 1
                    self.condition -= 0.1


class Nuvens(mesa.agent.AgentSet):
    def __init__(self, model, num_nuvens):
        super().__init__(model, num_nuvens)

    def do_step(self):
        # Definindo o ponto inicial para a nuvem
        x = random.randint(3, self.model.grid.width - 8)
        y = random.randint(3, self.model.grid.height - 8)

        # Definindo as posições ao redor da nuvem
        grid4x4 = [(x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)]
        
        # Garantir que o número de nuvens a serem movidas seja limitado ao número de posições
        num_positions = len(grid4x4)  # O número de posições válidas é 4
        num_nuvens = len(self)  # Número de nuvens

        # Verifica se o número de nuvens é maior que o número de posições válidas e ajusta
        num_to_move = min(num_positions, num_nuvens)  # Move no máximo 4 nuvens

        # Iteração sobre as nuvens
        for i in range(num_to_move):
            nuvem = self[i]  # Pega a i-ésima nuvem da lista
            nuvem.model.grid.move_agent(nuvem, grid4x4[i])  # Move a nuvem para a posição
            nuvem.step()  # Executa o passo da nuvem
