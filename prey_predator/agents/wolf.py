from mesa import Agent
from prey_predator.random_walk import RandomWalker
from prey_predator.agents.grass import GrassPatch
import prey_predator.agents.sheep as sheep
import numpy as np


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """
    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.pos = pos


    def check_if_alive(self):
        if self.energy<=0:
            cell_contents = self.model.grid.get_cell_list_contents([self.pos])
            no_grass = True
            for agent in cell_contents:
                if isinstance(agent,GrassPatch) :
                    agent.countdown=max(0,agent.countdown-2)
                    no_grass = False
                break
                
            if no_grass:
                self.model.create_grass(self.pos, fully_grown_value= False)

            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)


    def standard_wolf_energy(self,agent):
        self.energy +=  self.model.wolf_gain_from_food
        self.model.schedule.remove(agent)
        self.model.grid.remove_agent(agent)
    def capped_wolf_energy(self,agent):
        """
        If wolf is full of energy, do not eat sheep. Else, eat sheep and obtain part of its' energy.
        """
        if self.energy >= 10 :
            return
        else :
            self.energy += max(agent.energy//2,3)
            self.model.schedule.remove(agent)
            self.model.grid.remove_agent(agent)
            return

    def eat(self):
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_contents:
            if isinstance(agent,sheep.Sheep) :
                self.capped_wolf_energy(agent)
                #self.standard_wolf_energy(self,agent)
                break

    def closest_sheep_move(self):
        positions = []
        possible_positions = self.model.grid.get_neighborhood( self.pos, moore=True, include_center=False)
        for position in possible_positions:
            cell_contents = self.model.grid.get_cell_list_contents([position])
            for agent in cell_contents:
                if isinstance(agent,sheep.Sheep):
                    positions.append(position)
                    break
        if len(positions) > 0:
            position = self.random.choice(positions)
        else : 
            position = self.random.choice(possible_positions)

        self.model.grid.move_agent(self,position)




    def reproduce(self):
        """
        Initial reproduction process, if energy is sufficient, reproduce alone.
        """
        # if energy > 2 : reproduce ... 
        if self.energy >=2 and self.random.random() <= self.model.wolf_reproduce :
            self.energy //= 2
            new_wolf_agent = Wolf(unique_id = self.model.next_id(),
                                    pos = self.pos,
                                    model = self.model,
                                    moore = self.moore,
                                    energy= self.energy)
            self.model.schedule.add(new_wolf_agent)
            self.model.grid.place_agent(new_wolf_agent,self.pos)

    
    def realistic_reproduction(self):
        """
        Modelising reproduction with 2 wolfs rather than 1...
        """
        if self.energy > self.model.wolf_reproduction_minimal_energy :
            cell_contents = self.model.grid.get_cell_list_contents([self.pos])
            for agent in cell_contents:
                    if isinstance(agent,Wolf):

                        self.energy //= 2
                        new_wolf_agent = Wolf(unique_id = self.model.next_id(),
                                                pos = self.pos,
                                                model = self.model,
                                                moore = self.moore,
                                                energy= self.energy)
                        self.model.schedule.add(new_wolf_agent)
                        self.model.grid.place_agent(new_wolf_agent,self.pos)
                        break # can only reproduce once per timestep



    def move_to_reproduce(self):
        """
        If can reproduce, search for a mate in the closest cells that can also reproduce. If not found, will try to eat closest sheep
        """
        if self.energy > self.model.wolf_reproduction_minimal_energy:
            positions = []
            possible_positions = self.model.grid.get_neighborhood( self.pos, moore=True, include_center=False)
            for position in possible_positions:
                cell_contents = self.model.grid.get_cell_list_contents([position])
                for agent in cell_contents:
                    if isinstance(agent,Wolf):
                        if agent.energy > agent.model.wolf_reproduction_minimal_energy :
                            positions.append(position)
                            break
            if len(positions) > 0:
                position = self.random.choice(positions)
                self.model.grid.move_agent(self,position)
            else : 
                self.closest_sheep_move()
            

    def step(self):
        
        self.wants_to_reproduce = np.random.choice([True,False],1,p=[0.2,0.8])

        if self.wants_to_reproduce:
            print("want to reproduce")
            self.move_to_reproduce()
            self.energy -=1
            self.realistic_reproduction()
        else:
            print("wants to eat")
            self.closest_sheep_move()
            self.energy -=1
    
        self.eat()
        self.check_if_alive()