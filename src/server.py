import mesa
from .agent import TreeCell, Fireman, River, Terra, cloud, Birds
from .model import ForestFire
from pathlib import Path


# Dicionário de cores para os diferentes estados dos agentes
COLORS = {
    "Árvore Bem": "#00AA00",  # Verde para árvore saudável
    "Pegando Fogo": "#FF6F6F",  # Vermelho claro para árvore pegando fogo
    "Em Cinzas": "#000000",  # Preto para árvore queimada
    "Rio": "#ADD8E6",  # Azul claro para rio
    "Bombeiros": "#FFFF00",  # Amarelo para bombeiro
    "Nuvens": "#F8F8FF",  # Branco para nuvem
    "Terra": "#E5AA70",  # Cor de terra
    "Pássaros": "#0000FF",  # Azul escuro para pássaro
}


def get_tree_color(condition):
    """
    Retorna uma cor baseada na condição da árvore (0 a 1).
    O gradiente vai de verde (saudável) para vermelho (em chamas), depois para preto (queimada).
    """
    condition = max(
        0, min(1, condition)
    )  # Garantir que a condição está no intervalo [0, 1]

    if condition >= 0.7:  # Árvore saudável (verde)
        r = 0
        g = int(220 * (condition - 0.7) / 0.3)  # De verde para amarelo
        b = 0
    elif condition > 0.3:  # Árvore pegando fogo (vermelho)
        r = int(220 * ((condition - 0.3) / 0.4))  # De amarelo para vermelho
        # r = 220
        g = 0
        b = 0
    else:  # Árvore queimada (preto)
        r = 0
        g = 0
        b = 0

    # Garantir que r, g e b estão no intervalo [0, 255]
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    # Retorna a cor em formato hexadecimal
    return f"#{r:02x}{g:02x}{b:02x}"


def multi_agent_portrayal(agent):
    """
    Função para representar visualmente os agentes no grid. Dependendo do tipo de agente,
    ele será mostrado com uma cor e camada diferentes.
    """
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true"}

    # Se o agente não existir, retorna
    if agent is None:
        return portrayal

    # Representação do agente Terra
    if isinstance(agent, Terra):
        portrayal["Color"] = COLORS["Terra"]
        portrayal["Layer"] = 0

    # Representação do agente TreeCell
    elif isinstance(agent, TreeCell):
        condition = agent.condition / agent.life
        portrayal["Color"] = get_tree_color(condition)  # Use a função get_tree_color
        portrayal["Layer"] = 1

    # Representação do agente Fireman
    elif isinstance(agent, Fireman):
        portrayal["Color"] = (
            COLORS["Bombeiros"] if float(agent.condition) > 0 else "#000000"
        )
        portrayal["Layer"] = 2

    # Representação do agente River
    elif isinstance(agent, River):
        portrayal["Color"] = COLORS["Rio"] if float(agent.condition) > 0 else "#000000"
        portrayal["Layer"] = 3

    # Representação do agente Cloud
    elif isinstance(agent, cloud):
        portrayal["Color"] = COLORS["Nuvens"]
        portrayal["Layer"] = 4

    # Representação do agente Bird
    elif isinstance(agent, Birds):
        portrayal["Color"] = (
            COLORS["Pássaros"] if float(agent.condition) > 0 else "#000000"
        )
        portrayal["Layer"] = 4

    # Definindo as posições no grid
    portrayal["x"], portrayal["y"] = agent.pos
    return portrayal


# Configuração do CanvasGrid para visualização dos agentes
canvas_element = mesa.visualization.CanvasGrid(
    multi_agent_portrayal, 100, 100, 500, 500
)

# Configuração do gráfico de barras para visualização do estado das árvores
tree_chart = mesa.visualization.ChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)

# Configuração do gráfico de pizza para visualização das proporções dos estados dos agentes
pie_chart = mesa.visualization.PieChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)

# Definição dos parâmetros do modelo com sliders e opções para o usuário
model_params = {
    "height": 100,
    "width": 100,
    "tree_density": mesa.visualization.Slider(
        "Densidade de árvores", 0.8, 0.01, 1.0, 0.01
    ),
    "how_many_rivers": mesa.visualization.Choice(
        "Qtd de Rios", value=1, choices=[0, 1, 2, 3]
    ),
    "fire_focus": mesa.visualization.Slider(
        "Qtd de Focos de Incêndio", 5, 1, 20, 1
    ),  # Usuário pode escolher o número de focos de incêndio (1 a 20)
    # Adicionando o controle de nuvens (quantidade)
    "cloud_quantity": mesa.visualization.Slider(
        "Qtd de Nuvens",
        0,
        0,
        20,
        1,  # Slider para a quantidade de nuvens (1 a 20)
    ),
    "lightning_probability": mesa.visualization.Slider(
        "Probabilidade de Raio", 0.25, 0.0, 1.0, 0.01
    ),
    "rain_probability": mesa.visualization.Slider(
        "Probabilidade de Chuva", 0.25, 0.0, 1.0, 0.01
    ),
    "fireman_life": mesa.visualization.Slider("Vida Bombeiro", 200, 0, 1000, 1),
    "fireman_spawn_interval": mesa.visualization.Slider(
        "Intervalo Spawn Bombeiro", 10, 1, 100, 1
    ),
    "how_many_initial_fireman": mesa.visualization.Slider(
        "Qtd Inicial Bombeiros", 5, 0, 25, 1
    ),
    "new_fireman_rate": mesa.visualization.Slider("Qtd Novos Bombeiros", 1, 0, 15, 1),
    "burn_rate": mesa.visualization.Slider("Taxa de queima", 0.01, 0, 1, 0.001),
    "fire_propagation_rate": mesa.visualization.Slider(
        "Taxa Propagação do fogo entre Árvores", 0.2, 0, 1, 0.001
    ),
    "tree_life": mesa.visualization.Slider("Vida das Árvores", 1, 0, 100, 0.1),
    "how_many_birds": mesa.visualization.Slider("Qtd de Pássaro", 20, 0, 60, 1),
    "birds_spawn_interval": mesa.visualization.Slider(
        "Tempo de Spawn Pássaro", 10, 1, 100, 1
    ),
    "birds_life": mesa.visualization.Slider("Vida Pássaro", 100, 0, 1000, 1),
    "new_birds_rate": mesa.visualization.Slider("Qtd de Novos Pássaros", 1, 0, 15, 1),
    "fire_intensity": mesa.visualization.Slider(
        "Intensidade do Fogo", 0.1, 0.0, 1.0, 0.05
    ),
    "rain_intensity": mesa.visualization.Slider(
        "Intensidade da Chuva", 0.1, 0.0, 1.0, 0.05
    ),
}


class CustomPageHandler(mesa.visualization.PageHandler):
    def get(self):
        elements = self.application.visualization_elements
        for i, element in enumerate(elements):
            element.index = i
        self.render(
            "template.html",
            port=self.application.port,
            model_name=self.application.model_name,
            description=self.application.description,
            package_js_includes=list(self.application.package_js_includes.keys()),
            package_css_includes=list(self.application.package_css_includes.keys()),
            local_js_includes=list(self.application.local_js_includes.keys()),
            local_css_includes=list(self.application.local_css_includes.keys()),
            scripts=self.application.js_code,
        )


# Criação do servidor modular, que integra a visualização e o modelo
server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params
)

server.page_handler = (r"/", CustomPageHandler)

current_file_path = Path(__file__).resolve()
parent_dir = current_file_path.parent.parent

# server.settings["template_path"] = "/Av2-Prog2/template"

template_path = parent_dir / "template"
server.settings["template_path"] = str(template_path)
