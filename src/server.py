import mesa
from .agent import TreeCell, Fireman, River, Terra, cloud
from .model import ForestFire

# Dicionário de cores para os diferentes estados dos agentes
COLORS = {
    "Fine": "#00AA00",  # Verde para árvore saudável
    "On Fire": "#FF6F6F",  # Vermelho claro para árvore pegando fogo
    "Burned Out": "#000000",  # Preto para árvore queimada
    "River": "#ADD8E6",  # Azul claro para rio
    "Fireman": "#FFFF00",  # Amarelo para bombeiro
    "cloud": "#FFFFFF",  # Branco para nuvem
    "Terra": "#E5AA70",  # Cor de terra
}


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
        # A condição da árvore define a cor
        try:
            condition = float(agent.condition)
            if condition >= 0.7:
                portrayal["Color"] = COLORS["Fine"]
            elif condition > 0:
                portrayal["Color"] = COLORS["On Fire"]
            else:
                portrayal["Color"] = COLORS["Burned Out"]
        except ValueError:
            portrayal["Color"] = "#000000"  # Cor padrão caso haja erro na condição
        portrayal["Layer"] = 1

    # Representação do agente Fireman
    elif isinstance(agent, Fireman):
        portrayal["Color"] = (
            COLORS["Fireman"] if float(agent.condition) > 0 else "#000000"
        )
        portrayal["Layer"] = 2

    # Representação do agente River
    elif isinstance(agent, River):
        portrayal["Color"] = (
            COLORS["River"] if float(agent.condition) > 0 else "#000000"
        )
        portrayal["Layer"] = 3

    # Representação do agente Cloud
    elif isinstance(agent, cloud):
        portrayal["Color"] = COLORS["cloud"]
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
    "tree_density": mesa.visualization.Slider("Tree density", 0.8, 0.01, 1.0, 0.01),
    "how_many_rivers": mesa.visualization.Choice(
        "How many rivers", value=1, choices=[0, 1, 2, 3]
    ),
    "fire_focus": mesa.visualization.Slider(
        "Number of fire focuses", 5, 1, 20, 1
    ),  # Usuário pode escolher o número de focos de incêndio (1 a 20)
    # Adicionando o controle de nuvens (quantidade)
    "cloud_quantity": mesa.visualization.Slider(
        "Cloud quantity",
        2,
        0,
        20,
        1,  # Slider para a quantidade de nuvens (1 a 20)
    ),
    "fireman_life": mesa.visualization.Slider("Fireman life", 200, 0, 1000, 1),
    "fireman_spawn_interval": mesa.visualization.Slider('Spawn time of fireman', 10, 1, 100, 1),
    "how_many_initial_fireman": mesa.visualization.Slider("Quantity of initial fireman", 5, 0, 25, 1),
    "new_fireman_rate": mesa.visualization.Slider("Quantity of new fireman", 1, 0, 15, 1),
}

# Criação do servidor modular, que integra a visualização e o modelo
server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params
)
