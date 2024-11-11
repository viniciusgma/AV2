import mesa
from .agent import TreeCell, Fireman, Water, River
import random


class ForestFire(mesa.Model):
    """
    Simple Forest Fire model.
    """

    def __init__(
        self,
        width=100,
        height=100,
        tree_density=0.60,
        water_density=0.5,
        how_many_rivers=1,
        fire_focus=1,  # numero de focos de incêndio
        fireman_spawn_interval=10,  # Intervalo de tempo para criar novos bombeiros
    ):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        super().__init__()
        # Set up model objects
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, torus=False)

        self.datacollector = mesa.DataCollector(
            {
                "Fine": lambda model: model.count_condition(lambda c: float(c) > 0.7),
                "On Fire": lambda model: model.count_condition(
                    lambda c: 0 < float(c) <= 0.7
                ),
                "Burned Out": lambda model: model.count_condition(
                    lambda c: float(c) <= 0
                ),
                "Water": lambda model: model.count_condition_water(
                    lambda c: float(c) > 0
                ),
                "Firemen": lambda model: model.count_condition_fireman(
                    lambda c: float(c) > 0
                ),
            }
        )

        # Place a tree in each cell with Prob = density
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < tree_density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                self.grid.place_agent(new_tree, (x, y))
                self.schedule.add(new_tree)

        # Coloca os bombeiros
        center_x, center_y = width // 2, height // 2
        for i in range(8):
            pos = (center_x + i - 1, center_y + i - 1)
            new_fireman = Fireman(pos, self)
            self.grid.place_agent(new_fireman, pos)
            self.schedule.add(new_fireman)

        # Coloca os rios
        for rio in range(how_many_rivers):
            center_x, center_y = 2, random.choice(range(1, height))
            radius = 2
            increase_radius = [-2, -1, 0, 1, 2]
            while center_x <= 98 and center_y <= 98 and center_x >= 1 and center_y >= 1:
                for i in range(-radius, radius):
                    if (
                        center_x > 98
                        or center_y + i > 98
                        or center_x <= 0
                        or center_y + i <= 0
                    ):
                        continue
                    pos = (center_x, center_y + i)
                    river = River(pos, self)
                    self.grid.place_agent(river, pos)
                    self.schedule.add(river)

                center_x += 1
                center_y += random.choice([-1, 0, 1])
                radius += random.choice(increase_radius)

        # adiciona os focos de incêndio
        trees_on_fire = random.sample(
            [agent for agent in self.schedule.agents if isinstance(agent, TreeCell)],
            fire_focus,
        )
        for tree in trees_on_fire:
            tree.condition = 0.6  # Define condição de "On Fire" da árvore p/ pegar fogo

        self.running = True
        self.datacollector.collect(self)

        # **Configurações para criação automática de bombeiros**
        self.fireman_spawn_interval = (
            fireman_spawn_interval  # Intervalo de tempo para criar novos bombeiros
        )
        self.step_count = 0  # Contador de passos para controlar a criação de bombeiros

    def spawn_fireman(self):
        """Cria um novo bombeiro em uma posição aleatória da grade."""
        x, y = (
            random.randint(0, self.grid.width - 1),
            random.randint(0, self.grid.height - 1),
        )
        new_fireman = Fireman((x, y), self)
        self.grid.place_agent(new_fireman, (x, y))
        self.schedule.add(new_fireman)

    def step(self):
        """
        Advance the model by one step and add new firemen based on the interval.
        """
        self.schedule.step()
        self.datacollector.collect(self)
        self.step_count += 1

        # **Cria novos bombeiros em intervalos de tempo específicos**
        if self.step_count % self.fireman_spawn_interval == 0:
            self.spawn_fireman()

    def count_condition(model, condition_func):
        """ """
        count = sum(
            1
            for agent in model.schedule.agents
            if isinstance(agent, TreeCell) and condition_func(agent.condition)
        )
        return count

    def count_condition_fireman(model, condition_func):
        """ """
        count = sum(
            1
            for agent in model.schedule.agents
            if isinstance(agent, Fireman) and condition_func(agent.condition)
        )
        return count

    def count_condition_water(model, condition_func):
        """ """
        count = sum(
            1
            for agent in model.schedule.agents
            if isinstance(agent, Water) and condition_func(agent.condition)
        )
        return count
