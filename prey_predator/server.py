from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}
    portrayal["Shape"]="circle"
    portrayal["Filled"] ="true"
    portrayal["Layer"] = 0
    portrayal["r"]= 0.5
    
    if type(agent) is Sheep:
        portrayal["Color"]= "grey"
        # ... to be completed
        print("sheep")
    elif type(agent) is Wolf:
        # ... to be completed
        portrayal["Color"]= "black"
        print("wolf")
    elif type(agent) is GrassPatch:
        portrayal["Color"]= "green"

        # ... to be completed
        #print("grass")
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
server.port = 8521
