from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from prey_predator.parameters import model_params_definition
from prey_predator.agents.wolf import Wolf
from prey_predator.agents.sheep import Sheep
from prey_predator.agents.grass import GrassPatch
from prey_predator.model import WolfSheep
import os


def wolf_sheep_portrayal(agent):
    """
    Creates wolf/sheep/grass picture to add to the grid.
    """
    if agent is None:
        return
    portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "Layer": 0,
                    "r": 0.5}
    
    if type(agent) is Sheep:
        portrayal["Shape"] = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/sheep.png",
    elif type(agent) is Wolf:
        portrayal["Shape"] = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/wolf.png",
    elif type(agent) is GrassPatch:
        if agent.grown ==True:
            portrayal["Shape"] = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/grass.jpeg",
        else:
            portrayal["Shape"] = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/death_grass.jpg",
    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)

# colors for Wolves, Sheeps, and Grass
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"},{"Label": "Grass", "Color": "#519c3e"}]
)
chart_element.canvas_y_max = 300


# adding model params, with slides to change easily initializations.
model_params = model_params_definition()


server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8525
