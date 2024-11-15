import mesa
from .agent import TreeCell, Fireman, River, Terra, cloud, Birds
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
    "Birds": "#0000FF",  # Azul escuro para pássaro
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
        condition = agent.condition
        portrayal["Color"] = get_tree_color(condition)  # Use a função get_tree_color
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

    # Representação do agente Bird
    elif isinstance(agent, Birds):
        portrayal["Color"] = (
            COLORS["Birds"] if float(agent.condition) > 0 else "#000000"
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
        0,
        0,
        20,
        1,  # Slider para a quantidade de nuvens (1 a 20)
    ),
    "lightning_probability": mesa.visualization.Slider(
        "Lightning Probability", 0.25, 0.0, 1.0, 0.01
    ),
    "rain_probability": mesa.visualization.Slider(
        "Rain Probability", 0.25, 0.0, 1.0, 0.01
    ),
    "fireman_life": mesa.visualization.Slider("Fireman life", 200, 0, 1000, 1),
    "fireman_spawn_interval": mesa.visualization.Slider(
        "Spawn time of fireman", 10, 1, 100, 1
    ),
    "how_many_initial_fireman": mesa.visualization.Slider(
        "Quantity of initial fireman", 5, 0, 25, 1
    ),
    "new_fireman_rate": mesa.visualization.Slider(
        "Quantity of new fireman", 1, 0, 15, 1
    ),
    "burn_rate": mesa.visualization.Slider("Burn rate of the trees", 0.01, 0, 1, 0.001),
    "fire_propagation_rate": mesa.visualization.Slider(
        "Fire propagation rate between trees", 0.2, 0, 1, 0.001
    ),
    "tree_life": mesa.visualization.Slider("Life of the trees", 1, 0, 100, 0.1),
    "how_many_birds": mesa.visualization.Slider(
        "Quantity of initial fireman", 20, 0, 60, 1
    ),
    "birds_spawn_interval": mesa.visualization.Slider(
        "Spawn time of fireman", 10, 1, 100, 1
    ),
    "birds_life": mesa.visualization.Slider("Fireman life", 100, 0, 1000, 1),
    "new_birds_rate": mesa.visualization.Slider("Quantity of new fireman", 1, 0, 15, 1),
}

# Criação do servidor modular, que integra a visualização e o modelo
server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params
)

server.description = (  # por enquanto o \n não funciona
    "Modelo Forest Fire da biblioteca Mesa: _____________________________________________________ "
    "Lider: Vinicius Glowacki Maciel ____________________________________________________________ "
    "Equipe de Implementação: Gabriel Ferreira Silva, João Henrique Martins de Lima e Silva, Marcos Abílio "
    "Esmeraldo Melo, Richard Elias Soares Viana, Vinicius Glowacki Maciel ___________________________ "
    "Equipe de Visualização: Arthur Silva de Vasconcelos, Italo da Silva Santos, Igor Augusto Zwirtes, Jho-"
    "natas David de Lima Santos _______________________________________________________________ "
    "Equipe de Documentação: José Vitor Silva Model, Pedro Miguel Rocha Santos\n\n"
)
