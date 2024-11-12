import mesa
import random
from collections import deque


class Terra(mesa.Agent):
    def __init__(self, pos, model):
        """ """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = None


class TreeCell(mesa.Agent):
    """
    A tree cell. (teste workflow)

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = 1

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
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
    """representa um rio
    adiciona-se vida as arvoes que estao ate tres grids de distancia do rio.
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
        self.condition = 200

    def step(self):
        """

        Joga um raio em um raio de 1 grid. 5% de chance de ocorrer

        """
        num = random.randint(1, 100)
        if num <= 5:
            if self.condition > 0:
                for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                    if isinstance(neighbor, TreeCell):
                        if neighbor.condition:
                            neighbor.condition = 0.699  # coloca arvore em fogo

        """

        Raio da chuva de 5 grids.

        """
        if self.condition > 0:
            radius = self.model.grid.get_neighbors(self.pos, moore=True, radius=5)
            for coisa in radius:
                if isinstance(coisa, TreeCell) and self.condition > 0:
                    if coisa.condition:
                        coisa.condition += 0.7
                        self.condition -= 0.1
