import mesa
import random


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
                if neighbor.condition < 0.7:
                    self.condition -= 0.1


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
        # Chuva apriomara árvores e perde vida
        if self.condition > 0:
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if isinstance(neighbor, TreeCell) and neighbor.condition < 0.7:
                    neighbor.condition += 0.2
                    self.condition -= 0.1



class River(mesa.Agent):
    ''' representa um rio
    adiciona-se vida as arvoes que estao ate tres grids de distancia do rio.
    '''

    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = 2

    def step(self):
        if self.condition > 0:
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if isinstance(neighbor, TreeCell) and neighbor.condition < 0.7:
                    neighbor.condition += 0.2
                    self.condition -= 0.1
                if isinstance(neighbor, River) and neighbor.condition < 1.5:
                    neighbor.condition += 0.07
                    neighbor.condition -= 0.1
                for neigh in neighbor.model.grid.iter_neighbors(neighbor.pos, True):
                    if isinstance(neighbor, TreeCell) and neighbor.condition < 0.7:
                        neigh.condition += 0.05
                    if isinstance(neighbor, River) and neighbor.condition < 1.5:
                        neigh.condition += 0.07
                    
                    for neig in neigh.model.grid.iter_neighbors(neigh.pos, True):
                        if isinstance(neighbor, TreeCell) and neighbor.condition < 0.7:
                            neig.condition += 0.05
                        if isinstance(neighbor, River) and neighbor.condition < 1.5:
                            neig.condition += 0.07
                


