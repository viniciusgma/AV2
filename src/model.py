import mesa
from .agent import TreeCell, Fireman, Water


class ForestFire(mesa.Model):
    """
    Simple Forest Fire model.
    """

    def __init__(
        self,
        width=100,
        height=100,
        tree_density=0.09,
        water_density=0.4,
        fire_started_Y_axis=True,
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
        # Colocar estação de bombeiros

        # Place a tree in each cell with Prob = density
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < tree_density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.
                if fire_started_Y_axis:
                    if x == 0:
                        new_tree.condition = 0.6
                self.grid.place_agent(new_tree, (x, y))
                self.schedule.add(new_tree)

            else:
                if self.random.random() < water_density:
                    # Create a tree
                    new_water = Water((x, y), self)
                    self.grid.place_agent(new_water, (x, y))
                    self.schedule.add(new_water)

        # Coloca os bombeiros
        center_x, center_y = width // 2, height // 2
        for i in range(8):
            pos = (center_x + i - 1, center_y + i - 1)
            new_fireman = Fireman(pos, self)
            self.grid.place_agent(new_fireman, pos)
            self.schedule.add(new_fireman)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        self.datacollector.collect(self)

    #        if self.count_condition(lambda c: 0 < float(c) < 1) == 0:
    #            self.running = False

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
