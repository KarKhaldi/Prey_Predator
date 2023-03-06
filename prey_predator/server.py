from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep
import os


def wolf_sheep_portrayal(agent):
    if agent is None:
        return
    portrayal = {"Shape": "circle",
                               "Filled": "true",
                               "Layer": 0,
                               "r": 0.5}
    # portrayal["Shape"]="circle"
    # portrayal["Filled"] ="true"
    # portrayal["Layer"] = 3
    # portrayal["r"]= 0.5
    
    if type(agent) is Sheep:
        portrayal["Shape"] = f"{os.path.dirname(os.path.realpath(__file__))}/sheep.png",
        # ... to be completed
    elif type(agent) is Wolf:
        portrayal["Shape"] = f"{os.path.dirname(os.path.realpath(__file__))}/wolf.png",

    elif type(agent) is GrassPatch:
        if agent.grown ==True:
            portrayal["Shape"] = f"{os.path.dirname(os.path.realpath(__file__))}/grass.jpeg",
        else:
            portrayal["Shape"] = f"{os.path.dirname(os.path.realpath(__file__))}/death_grass.jpg",
        # ... to be completed
    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

model_params = {
    # ... to be completed
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8525
