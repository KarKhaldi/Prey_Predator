from mesa import Agent
from prey_predator.random_walk import RandomWalker
from prey_predator.agents.grass import GrassPatch
from prey_predator.agents.sheep import Sheep



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
        if self.energy >= 15 :
            return
        else :
            self.energy += max(agent.energy,3)
            print()
            self.model.schedule.remove(agent)
            self.model.grid.remove_agent(agent)
            return

    def eat(self):
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_contents:
            if isinstance(agent,Sheep) :
                self.capped_wolf_energy(agent)
                #self.standard_wolf_energy(self,agent)
                break


    def reproduce(self):
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


    def step(self):
        self.random_move()
        self.energy -=1
        self.reproduce()
        self.eat()
        self.check_if_alive()