import mesa
import random
from collections import deque


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
        if self.condition < 0.7:
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                neighbor.condition -= 0.05
                if neighbor.condition < 0.7:
                    self.condition -= 0.05


class Fireman(mesa.Agent):
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
        Se árvores vizinhas estão pegando fogo, o bombeiro apaga e
        perde 0.1 de vida por árvore apagada
        """
        if self.condition > 0:
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.condition < 0.7:
                    neighbor.condition += 0.2
                    self.condition -= 0.1

        x, y = self.pos
        new_pos = (x + random.randint(-1, 1), y + random.randint(-1, 1))
        self.model.grid.move_agent(self, new_pos)


class Water(mesa.Agent):
    """ """

    def __init__(self, pos, model):
        """ """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = 2

    def step(self):
        """ """
        # apriomara árvores e perde vida
        if self.condition > 0:
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if isinstance(neighbor, TreeCell) and neighbor.condition < 0.7:
                    neighbor.condition += 0.2
                    self.condition -= 0.1


class River(mesa.Agent):
    """representa um rio
    adiciona-se vida as arvoes que estao ate tres grids de distancia do rio.
    """

    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = 2

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
                elif isinstance(current, River) and current.condition <0.7:
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
        self.condition = 2

    def lightning(self):
        """

        Joga um raio em um raio de 1 grid.

        """
        if self.condition > 0:
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if isinstance(neighbor, TreeCell):
                    neighbor.condition = 0

    def rain(self):
        """

        Raio da chuva de 5 grids.

        """
        if self.condition > 0:
            radius = self.model.grid.get_neighbors(self.pos, moore=True, radius=5)
            for coisa in radius:
                if isinstance(coisa, TreeCell):
                    coisa.condition += 0.7
                    self.condition -= 0.1
