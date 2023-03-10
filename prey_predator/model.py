"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

# maybe put all the agents in a folder ??
from prey_predator.agents.grass import GrassPatch
from prey_predator.agents.sheep import Sheep
from prey_predator.agents.wolf import Wolf

from prey_predator.schedule import RandomActivationByBreed
import numpy as np


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """


    def __init__(
        self,
        height,width,
        initial_sheep,sheep_reproduce, sheep_gain_from_food, initial_sheep_energy,
        initial_wolves,wolf_reproduce,wolf_gain_from_food, initial_wolf_energy,
        grass_is_grown,grass_regrowth_time,
        **kwargs
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        
        # grid parameters
        self.height = height
        self.width = width
        self.grid = MultiGrid(self.height, self.width, torus=True)

        # sheep parameters
        self.initial_sheep = initial_sheep
        self.sheep_reproduce = sheep_reproduce
        self.sheep_gain_from_food = sheep_gain_from_food
        self.initial_sheep_energy = initial_sheep_energy

        #wolf parameters
        self.initial_wolves = initial_wolves
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.initial_wolf_energy = initial_wolf_energy
        self.wolf_reproduction_minimal_energy = 5

        #grass parameters
        self.grass = grass_is_grown
        self.grass_regrowth_time = grass_regrowth_time
        self.grass_here = 0 
        self.where_are_grasses = np.zeros((self.height,self.width))

        #scheduler and data collector
        self.schedule = RandomActivationByBreed(self)
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
                "Grass": lambda m: m.schedule.get_breed_count(GrassPatch),
            }
        )

        # Create sheep:
        for i in range(self.initial_sheep):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            sheep_agent = Sheep(unique_id=self.next_id(),
                                pos =(x,y), 
                                model = self,
                                moore=True,
                                energy = self.initial_sheep_energy
                                )
            self.schedule.add(sheep_agent)
            self.grid.place_agent(sheep_agent,(x,y))
        # Create wolves
        for i in range(self.initial_wolves ):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            wolf_agent =Wolf(unique_id=self.next_id(),
                              pos = (x,y),
                              model = self, 
                              moore=True ,
                              energy = self.initial_wolf_energy
                            )
            self.schedule.add(wolf_agent)
            self.grid.place_agent(wolf_agent,(x,y))
 
        # Create grass patches

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                pass
                is_here = self.random.choice([True, False])
                if is_here:
                    self.create_grass((x,y))
                else : 
                    pass



    def step(self):

        self.schedule.step()
        # Collect data
        self.datacollector.collect(self)

        for j in range(20):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            if self.where_are_grasses[x,y] == 0:
                self.create_grass((x,y))

    
    def create_grass(self, pos, fully_grown_value = True):
        grass_agent = GrassPatch(self.next_id(),
                                    pos = pos,
                                    model = self,
                                    fully_grown = fully_grown_value,
                                    countdown = self.grass_regrowth_time
                                    )
        self.schedule.add(grass_agent)
        self.grid.place_agent(grass_agent,pos)
        self.where_are_grasses[pos] = 1
    
    def run_model(self, step_count=200):

        for i in range(step_count):
            ## take randomly a position where there is no grass
            
            self.step()

