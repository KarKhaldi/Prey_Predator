
from mesa.visualization.UserParam import UserSettableParameter

def model_params_definition():
    model_params = {'description': 'A model for simulating wolf and sheep (predator-prey) ecosystem modelling.', 
                'height': 20,
                'width': 20, 
                'initial_sheep':  UserSettableParameter("slider", "initial_sheep", 100, 20, 200, 5),
                'sheep_reproduce': UserSettableParameter("slider", "sheep_reproduce", 0.05, 0.01, 1, 0.01),
                'sheep_gain_from_food': UserSettableParameter("slider", "sheep_gain_from_food", 4, 1, 30, 1), 
                'initial_sheep_energy': UserSettableParameter("slider", "initial_sheep_energy", 5, 1, 30, 1),
                'initial_wolves': UserSettableParameter("slider", "initial_wolves", 50, 10, 200, 5), 
                'wolf_reproduce': UserSettableParameter("slider", "wolf_reproduce", 0.05, 0.01, 1, 0.01), 
                'wolf_gain_from_food': UserSettableParameter("slider", "wolf_gain_from_food", 20, 1, 100, 1), 
                'initial_wolf_energy': UserSettableParameter("slider", "initial_wolf_energy", 5, 1, 30, 1), 
                'grass_is_grown': 1,
                'grass_regrowth_time': UserSettableParameter("slider", "grass_regrowth_time", 10, 1, 30, 1)}
    return model_params