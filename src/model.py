import mesa
import random
from .agent import TreeCell, Fireman, River, Terra, cloud, Nuvens

class ForestFire(mesa.Model):
    """
    Simple Forest Fire model.
    """

    def __init__(
        self,
        width=100,
        height=100,
        tree_density=0.60,
        how_many_rivers=1,
        fire_focus=5,  # número de focos de incêndio
        fireman_spawn_interval=10,  # Intervalo de tempo para criar novos bombeiros
        cloud_quantity=5,  # Novo parâmetro para o número de nuvens
        lightning_probability=0.25,  # Probabilidade de raio
        rain_probability=0.25,  # Probabilidade de chuva
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

        # Configura as probabilidades de raio e chuva
        self.lightning_probability = lightning_probability
        self.rain_probability = rain_probability

        self.datacollector = mesa.DataCollector(
            {
                "Fine": lambda model: model.count_condition(
                    TreeCell, lambda c: float(c) > 0.7
                ),
                "On Fire": lambda model: model.count_condition(
                    TreeCell, lambda c: 0 < float(c) <= 0.7
                ),
                "Burned Out": lambda model: model.count_condition(
                    TreeCell, lambda c: float(c) <= 0
                ),
                "Firemen": lambda model: model.count_condition(
                    Fireman, lambda c: float(c) > 0
                ),
                "Rivers": lambda model: model.count_condition(
                    River, lambda c: float(c) > 0
                ),
                "Terra": lambda model: model.count_condition(Terra, lambda c: True),
            }
        )

        # Coloca as árvores no grid
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < tree_density:
                # Cria uma árvore
                new_tree = TreeCell((x, y), self)
                self.grid.place_agent(new_tree, (x, y))
                self.schedule.add(new_tree) 
            else:
                new_terra = Terra((x, y), self)
                self.grid.place_agent(new_terra, (x, y))

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

        # Adiciona os focos de incêndio
        trees_on_fire = random.sample(
            [agent for agent in self.schedule.agents if isinstance(agent, TreeCell) and agent.condition == 1.0],
            fire_focus,
        )
        for tree in trees_on_fire:
            tree.condition = 0.6  # Define condição de "On Fire" para as árvores

        # Adicionar nuvens com base no valor do slider
        self.create_clouds(cloud_quantity)

        self.running = True
        self.datacollector.collect(self)

        # **Configurações para criação automática de bombeiros**
        self.fireman_spawn_interval = (
            fireman_spawn_interval  # Intervalo de tempo para criar novos bombeiros
        )
        self.step_count = 0  # Contador de passos para controlar a criação de bombeiros

    def create_clouds(self, cloud_quantity):
        """
        Cria o número de nuvens baseado no valor fornecido pelo usuário no slider.
        """
        self.nuvens = []
        for _ in range(cloud_quantity):  # Cloud quantity agora é o número de nuvens
            nuvens = []
            # Geração de posições aleatórias para as nuvens dentro do grid
            x = random.randint(7, self.grid.width - 8)
            y = random.randint(7, self.grid.height - 8)

            # Gera 4 posições ao redor da posição (x, y)
            grid4x4 = [(x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)]

            # Filtra as posições para garantir que estão dentro dos limites do grid
            valid_positions = [
                pos
                for pos in grid4x4
                if 0 <= pos[0] < self.grid.width and 0 <= pos[1] < self.grid.height
            ]

            # Coloca as nuvens apenas nas posições válidas
            for pos in valid_positions:
                new_cloud = cloud(pos, self)
                nuvens.append(new_cloud)
                self.grid.place_agent(new_cloud, pos)

            self.nuvens.append(Nuvens(nuvens, self))

    def spawn_fireman(self):
        """Cria um novo bombeiro em uma posição aleatória da grade."""
        x, y = (
            random.randint(0, self.grid.width - 2),
            random.randint(0, self.grid.height - 2),
        )
        new_fireman = Fireman((x, y), self)
        self.grid.place_agent(new_fireman, (x, y))
        self.schedule.add(new_fireman)

    def step(self):
        """
        Avança o modelo em um passo e adiciona novos bombeiros com base no intervalo.
        """
        self.schedule.step()
        self.datacollector.collect(self)
        self.step_count += 1

        for nuvens in self.nuvens:
            nuvens.do_step()

        # **Cria novos bombeiros em intervalos de tempo específicos**
        if self.step_count % self.fireman_spawn_interval == 0:
            self.spawn_fireman()

    def count_condition(self, obj_class, condition_func):
        """Contagem de agentes com base em uma condição"""
        count = sum(
            1
            for agent in self.schedule.agents
            if isinstance(agent, obj_class) and condition_func(agent.condition)
        )
        return count
