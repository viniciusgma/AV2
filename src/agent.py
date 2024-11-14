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
    """

    def __init__(self, pos, model, burn_rate, fire_rate, life):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = life  # A árvore começa saudável
        self.life = life  # Quantidade total de vida para referência
        self.brn = burn_rate  # Velocidade de queima
        self.fire = fire_rate  # Velocidade de propagação do fogo

    def step(self):
        """
        Se a árvore está pegando fogo, ela espalha fogo para as árvores mais próximas.
        A condição da árvore vai diminuindo conforme o fogo avança.
        """
        if self.condition > 0:
            if self.condition >= 0.7 * self.life:
                # A árvore está saudável e pode começar a pegar fogo
                for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                    if (
                        isinstance(neighbor, TreeCell)
                        and neighbor.condition < 0.7 * self.life
                        and neighbor.condition > 0.3 * self.life
                    ):
                        self.condition -= (
                            self.brn * 0.5
                        )  # A árvore começa a ser afetada pelo fogo

            elif 0.3 * self.life < self.condition <= 0.7 * self.life:
                # A árvore está pegando fogo, espalha o fogo para os vizinhos
                for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                    if (
                        isinstance(neighbor, TreeCell)
                        and neighbor.condition > 0.7 * self.life
                    ):
                        neighbor.condition -= self.fire  # Espalha o fogo
                        self.condition -= self.brn  # A árvore queima um pouco
                    else:
                        self.condition -= self.brn
            else:
                # arvore em cinzas
                self.condition -= self.brn

        else:
            self.condition = 0  # Quando a árvore é queimada, sua condição vai a 0


class Fireman(mesa.Agent):
    """
    Classe para o bombeiro, que agora usa BFS para encontrar o fogo mais próximo.
    """

    def __init__(self, pos, model, life, tree_life):
        """
        Cria um novo bombeiro.

        Args:
            pos: Coordenadas iniciais do bombeiro no grid.
            model: Referência ao modelo.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = life  # Vida do bombeiro
        self.tree_life = tree_life

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
                    if (
                        isinstance(neighbor, TreeCell)
                        and 0 < neighbor.condition < 0.7 * self.tree_life
                    ):
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
                if (
                    isinstance(neighbor, TreeCell)
                    and neighbor.condition < 0.7 * self.tree_life
                ):
                    neighbor.condition += 0.3  # Apaga um pouco o fogo
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
            while len(visited) <= 6:
                current = dq.popleft()
                dq.extend(current.model.grid.iter_neighbors(current.pos, True))
                if current not in visited:
                    visited.append(current)
                if current not in visited:
                    visited.append(current)
                if (
                    isinstance(current, TreeCell)
                    and current.condition < 0.7 * current.life
                ):
                    current.condition += 0.3 * current.life
                elif isinstance(current, River) and current.condition < 0.7:
                    current.condition += 0.05


class cloud(mesa.Agent):
    """
    A nuvem possui duas ações possíveis:

    lightning - joga um raio exatamente na árvore da mesma célula, fazendo ela pegar fogo
    rain - faz chover em um raio específico, aumentando a vida de todas as árvores
    e fazendo o fogo parar se existir.
    """

    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = 2000
        # Recupera as probabilidades de raio e chuva do modelo
        self.lightning_probability = model.lightning_probability
        self.rain_probability = model.rain_probability

    def step(self):
        """
        Joga um raio ou chuva baseado nas probabilidades definidas pelo usuário.
        """

        num = random.random()  # Gera um número aleatório entre 0 e 1
        if num <= self.lightning_probability:
            # Se a probabilidade para raio for atendida, um raio cai em uma árvore
            if self.condition > 0:
                for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                    if isinstance(neighbor, TreeCell):
                        neighbor.condition = 0.6  # Coloca a árvore em fogo

        elif num <= self.lightning_probability + self.rain_probability:
            # Se a probabilidade para chuva for atendida, faz chover
            radius = self.model.grid.get_neighbors(self.pos, moore=True, radius=2)
            for coisa in radius:
                if isinstance(coisa, TreeCell):
                    coisa.condition += coisa.life  # Aumenta a condição da árvore
                    self.condition -= 0.1  # Diminui a condição da nuvem
                elif isinstance(coisa, River):
                    coisa.condition += 1


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
            nuvem.model.grid.move_agent(
                nuvem, grid4x4[i]
            )  # Move a nuvem para a posição
            nuvem.step()  # Executa o passo da nuvem


class Bird(mesa.Agent):
    """
    Classe Bird que representa os pássaros responsáveis por regenerar terra.
    """

    def __init__(self, pos, model):
        """ "
        Inicia o pássaro.

        Args:
            pos: Posição inicial do pássaro no grid.
            model: Referência ao modelo.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = 100  # Vida do passaro

    def bfs_to_land(self):
        """
        Executa uma busca em largura (BFS) para encontrar a célula de terra mais próxima.
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

                    # Se a célula do vizinho for terra
                    if isinstance(neighbor, Terra):
                        return neighbor.pos  # retorna a posição da terra mais próxima
        return (1, 1)  # nenhuma terra encontrada

    def step(self):
        """
        Ação do pássaro em cada passo: usa a BFS para encontrar a terra mais próxima e se move na direção dela.
        """
        # Tenta encontrar a posição de terra
        target_pos = self.bfs_to_land()

        # Se houver terra, move-se na direção dela
        if target_pos:
            x, y = self.pos
            tx, ty = target_pos

            # Movimenta-se em direção da terra
            new_pos = (
                x + (1 if tx > x else -1 if tx < x else 0),
                y + (1 if ty > y else -1 if ty < y else 0),
            )

            self.model.grid.move_agent(self, new_pos)

            # Se o pássaro está próximo de uma árvore em chamas, ele perde vida
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if isinstance(neighbor, TreeCell) and neighbor.condition < 0.7:
                    self.condition -= 2  # Perde vida ao passar pelo fogo

            # Transformação de terra em árvore
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if isinstance(neighbor, Terra):
                    new_tree = TreeCell(neighbor.pos, self.model)
                    self.model.grid.remove_agent(neighbor)  # Remove a terra
                    self.model.grid.place_agent(
                        new_tree, neighbor.pos
                    )  # Coloca a árvore
                    self.model.schedule.add(
                        new_tree
                    )  # Adiciona a nova árvore ao agendamento
                    self.condition -= 0.1  # Perde vida ao transformar terra em árvore

        # Se não há terra, move-se aleatoriamente
        else:
            x, y = self.pos
            new_pos = (x + random.randint(-1, 1), y + random.randint(-1, 1))
            self.model.grid.move_agent(self, new_pos)

        # Remove o pássaro se ele morreu
        if self.condition <= 0:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
