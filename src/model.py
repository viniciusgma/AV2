import mesa
import random
from .agent import TreeCell, Fireman, River, Terra, cloud, Nuvens, Birds


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
        fireman_life=200,  # Quantidade de vida dos bombeiros
        cloud_quantity=5,  # Novo parâmetro para o número de nuvens
        lightning_probability=0.25,  # Probabilidade de raio
        rain_probability=0.25,  # Probabilidade de chuva
        how_many_initial_fireman=5,  # Quantidade de bombeiros gerados no início da simulação
        new_fireman_rate=1,  # Quantidade de novos bombeiros que aparecem a cada intervalo
        burn_rate=0.1,  # Intensidade do fogo
        fire_propagation_rate=0.2,  # Velocidade de propagação do fogo
        tree_life=1.0,  # Quantidade de vida das árvores
        how_many_birds=20,  # Quantidade inicial de pássaros
        birds_spawn_interval=10,  # Intervalo de tempo para criar novos pássaros
        birds_life=100,  # Quantidade de vida dos pássaros
        new_birds_rate=1,  # Quantidade de novos pássaros que surgem a cada intervalo
        fire_intensity=1.0,  # Intensidade do fogo
        rain_intensity=1.0,  # Intensidade da chuva
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

        # Configurações de intensidade de fogo e chuva
        self.fire_intensity = fire_intensity
        self.rain_intensity = rain_intensity
        self.lightning_probability = lightning_probability
        self.rain_probability = rain_probability
        self.kill = []

        self.datacollector = mesa.DataCollector(
            {
                "Árvore Bem": lambda model: model.count_condition(
                    TreeCell, lambda c: float(c) > 0.7
                ),
                "Pegando Fogo": lambda model: model.count_condition(
                    TreeCell, lambda c: 0.3 < float(c) <= 0.7
                ),
                "Em Cinzas": lambda model: model.count_condition(
                    TreeCell, lambda c: 0 <= float(c) <= 0.3
                ),
                "Bombeiros": lambda model: model.count_condition(
                    Fireman, lambda c: float(c) > 0
                ),
                "Rio": lambda model: model.count_condition(
                    River, lambda c: float(c) > 0
                ),
                "Terra": lambda model: model.count_condition(Terra, lambda c: True),
                "Pássaros": lambda model: model.count_condition(
                    Birds, lambda c: float(c) > 0
                ),
            }
        )

        # Coloca as árvores no grid
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < tree_density:
                # Cria uma árvore
                new_tree = TreeCell(
                    (x, y), self, burn_rate, fire_propagation_rate, tree_life
                )
                self.grid.place_agent(new_tree, (x, y))
                self.schedule.add(new_tree)
            else:
                new_terra = Terra(
                    (x, y), self, burn_rate, fire_propagation_rate, tree_life
                )
                self.grid.place_agent(new_terra, (x, y))
                self.schedule.add(new_terra)

        # Coloca os bombeiros
        center_x, center_y = width // 2, height // 2
        for i in range(how_many_initial_fireman):
            pos = (center_x + i - 1, center_y + i - 1)
            new_fireman = Fireman(pos, self, fireman_life, tree_life)
            self.grid.place_agent(new_fireman, pos)
            self.schedule.add(new_fireman)

        # Coloca os pássaros
        for i in range(how_many_birds):
            pos = (
                random.randint(0, self.grid.width - 1),
                random.randint(0, self.grid.height - 1),
            )
            bird = Birds(pos, self, birds_life, tree_life)
            self.grid.place_agent(bird, pos)
            self.schedule.add(bird)

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
            [
                agent
                for agent in self.schedule.agents
                if isinstance(agent, TreeCell) and agent.condition == tree_life
            ],
            fire_focus,
        )
        for tree in trees_on_fire:
            tree.condition = (
                0.6 * tree.life
            )  # Define condição de "On Fire" para as árvores

        # Adicionar nuvens com base no valor do slider
        self.create_clouds(cloud_quantity)

        self.running = True
        self.datacollector.collect(self)

        # **Configurações para criação automática de bombeiros**
        self.fireman_spawn_interval = (
            fireman_spawn_interval  # Intervalo de tempo para criar novos bombeiros
        )
        self.step_count = 0  # Contador de passos para controlar a criação de bombeiros
        self.fireman_life = (
            fireman_life  # Define a quantidade de vida dos bombeiros com base no slider
        )
        self.new_fireman_rate = new_fireman_rate  # Define a quantidade de novos bombeiros que surgem a cada intervalo
        self.tree_life = tree_life

        # Configurações para criação automática de pássaros
        self.birds_spawn_interval = (
            birds_spawn_interval  # Intervalo de tempo para criar novos pássaros
        )
        self.step_count = 0  # Contador de passos para controlar a criação de pássaros
        self.bird_life = (
            birds_life  # Define a quantidade de vida dos pássaros com base no slider
        )
        self.new_birds_rate = new_birds_rate  # Define a quantidade de novos pássaros que surgem a cada intervalo

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

    def spawn_fireman(self, fireman_life, new_fireman_rate, tree_life):
        """Cria um novo bombeiro em uma posição aleatória da grade."""
        for _ in range(new_fireman_rate):
            x, y = (
                random.randint(0, self.grid.width - 2),
                random.randint(0, self.grid.height - 2),
            )
            new_fireman = Fireman((x, y), self, fireman_life, tree_life)
            self.grid.place_agent(new_fireman, (x, y))
            self.schedule.add(new_fireman)

    def spawn_birds(self, bird_life, new_birds_rate, tree_life):
        """Cria um novo pássaro em uma posição aleatória da grade."""
        for _ in range(new_birds_rate):
            x, y = (
                random.randint(0, self.grid.width - 2),
                random.randint(0, self.grid.height - 2),
            )
            new_birds = Birds((x, y), self, bird_life, tree_life)
            self.grid.place_agent(new_birds, (x, y))
            self.schedule.add(new_birds)

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
            self.spawn_fireman(self.fireman_life, self.new_fireman_rate, self.tree_life)

        # Cria novos pássaros em intervalos de tempo específicos
        if self.step_count % self.birds_spawn_interval == 0:
            self.spawn_birds(self.bird_life, self.new_birds_rate, self.tree_life)

    def count_condition(self, obj_class, condition_func):
        """Contagem de agentes com base em uma condição"""
        count = sum(
            1
            for agent in self.schedule.agents
            if (isinstance(agent, obj_class) and condition_func(agent.condition))
        )
        return count
