import mesa
from .agent import TreeCell, Fireman, River
from .model import ForestFire

COLORS = {
    "Fine": "#00AA00",  # Green
    "On Fire": "#FF6F6F",  # Light Red
    "Burned Out": "#000000",  # Black
    "river": "#ADD8E6",  # Blue
    "Fireman": "#FFFF00",  # Yellow
    "Nuvem": "#FFFFFF",  # White
}


def multi_agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true"}

    if isinstance(agent, TreeCell):
        if float(agent.condition) >= 0.7:
            portrayal["Color"] = "#00AA00"  # Fine (Green)
        elif float(agent.condition) > 0:
            portrayal["Color"] = "#880000"  # On Fire (Red)
        else:
            portrayal["Color"] = "#000000"  # Burned Out (Black)
        portrayal["Layer"] = 0

    elif isinstance(agent, Fireman):
        portrayal["Color"] = "#FFFF00" if float(agent.condition) > 0 else "#000000"
        portrayal["Layer"] = 1

    elif isinstance(agent, River):
        if float(agent.condition) > 0:
            portrayal["Color"] = "#ADD8E6"
        else:
            portrayal["Color"] = "#000000"
        portrayal["Layer"] = 3

    portrayal["x"], portrayal["y"] = agent.pos
    return portrayal


canvas_element = mesa.visualization.CanvasGrid(
    multi_agent_portrayal, 100, 100, 500, 500
)
tree_chart = mesa.visualization.ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
pie_chart = mesa.visualization.PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

model_params = {
    "height": 100,
    "width": 100,
    "tree_density": mesa.visualization.Slider("Tree density", 0.65, 0.01, 1.0, 0.01),
    "water_density": mesa.visualization.Slider("Water density", 0.3, 0.01, 1.0, 0.01),
    "how_many_rivers": mesa.visualization.Choice(
        "how_many_rivers", value=1, choices=[0, 1, 2, 3]
    ),
    "fire_focus": mesa.visualization.Slider(
        "Number of fire focuses", 1, 1, 20, 1
    ),  # usuario pode escolher número de focos do fogo com um slider de 1 até 20 focos
}

server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params
)
