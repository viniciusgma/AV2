import mesa
import random


def normalize_condition(value, min_value=0, max_value=1):
    """

    Garantir que a condição do agente esteja entre os valores mínimo e máximo.

    """
    return max(min(value, max_value), min_value)


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
                neighbor.condition -= 0.1
                neighbor.condition = normalize_condition(neighbor.condition)
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
                    self.condition = normalize_condition(self.condition)

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
        # Chuva aprimora árvores e perde vida
        if self.condition > 0:
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if isinstance(neighbor, TreeCell) and neighbor.condition < 0.7:
                    neighbor.condition += 0.2
                    self.condition -= 0.2  # nerfado de 0.1 -> 0.2
                    self.condition = normalize_condition(self.condition, 0, 2)
                    neighbor.condition = normalize_condition(neighbor.condition)


class River(mesa.Agent):
    """representa um rio
    adiciona-se vida as arvoes que estao ate tres grids de distancia do rio.
    """

    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = 1.5  # nerfado de 2 -> 1.5

    def step(self):
        if self.condition > 0:
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if isinstance(neighbor, TreeCell) and neighbor.condition < 0.7:
                    neighbor.condition += 0.2
                    self.condition -= 0.1
                    self.condition = normalize_condition(self.condition, 0, 1.5)
                if isinstance(neighbor, River) and neighbor.condition < 1.5:
                    neighbor.condition += 0.07
                    neighbor.condition -= 0.1
                    neighbor.condition = normalize_condition(neighbor.condition)
                for neigh in neighbor.model.grid.iter_neighbors(neighbor.pos, True):
                    if isinstance(neighbor, TreeCell) and neighbor.condition < 0.7:
                        neigh.condition += 0.05
                        neigh.condition = normalize_condition(neigh.condition)
                    if isinstance(neighbor, River) and neighbor.condition < 1.5:
                        neigh.condition += 0.07
                        neigh.condition = normalize_condition(neigh.condition)

                    for neig in neigh.model.grid.iter_neighbors(neigh.pos, True):
                        if isinstance(neighbor, TreeCell) and neighbor.condition < 0.7:
                            neig.condition += 0.05
                            neig.condition = normalize_condition(neig.condition)
                        if isinstance(neighbor, River) and neighbor.condition < 1.5:
                            neig.condition += 0.07
                            neig.condition = normalize_condition(neig.condition)


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

    def step(self):
        """

        Joga um raio em um raio de 1 grid. 5% de chance de ocorrer

        """
        num = random.randint(1, 100)
        if num <= 5:
            if self.condition > 0:
                for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                    if isinstance(neighbor, TreeCell):
                        neighbor.condition = 0  # coloca arvore em fogo

        """

        Raio da chuva de 5 grids.

        """
        if self.condition > 0:
            radius = self.model.grid.get_neighbors(self.pos, moore=True, radius=5)
            for coisa in radius:
                if isinstance(coisa, TreeCell) and self.condition > 0:
                    coisa.condition += 0.7
                    self.condition -= 0.1
                    coisa.condition = normalize_condition(coisa.condition)
