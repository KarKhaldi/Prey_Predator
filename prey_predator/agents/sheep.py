from mesa import Agent
from prey_predator.random_walk import RandomWalker
from prey_predator.agents.grass import GrassPatch
# from prey_predator.agents.wolf import Wolf



class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """
    # to do : change eat to not change value of grass 
    # but call a function in grass or from model.
    # cf cours 1 de SMA
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

    
    def eat(self):

        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_contents:
            if isinstance(agent,GrassPatch) and agent.grown :
                self.energy += self.model.sheep_gain_from_food 
                agent.grown = False
                break

    def reproduce(self):
        # if energy > 2 : reproduce ... 
        if self.energy >=2 and self.random.random() <= self.model.sheep_reproduce :
            self.energy //= 2
            new_sheep_agent = Sheep(unique_id = self.model.next_id(),
                                    pos = self.pos,
                                    model = self.model,
                                    moore = self.moore,
                                    energy= self.energy)
            self.model.schedule.add(new_sheep_agent)
            self.model.grid.place_agent(new_sheep_agent,self.pos)

    def target_grass(self):
        positions = []
        possible_positions = self.model.grid.get_neighborhood( self.pos, moore=True, include_center=False)
        for position in possible_positions:
            cell_contents = self.model.grid.get_cell_list_contents([position])
            for agent in cell_contents:
                if isinstance(agent,GrassPatch) and agent.grown:
                    positions.append(position)
                    break
        if len(positions) > 0:
            position = self.random.choice(positions)
        else : 
            position = self.random.choice(possible_positions)

        self.model.grid.move_agent(self,position)
    
    def avoid_wolves(self):
        positions = []
        possible_positions = self.model.grid.get_neighborhood( self.pos, moore=True, include_center=False)
        for position in possible_positions:
            cell_contents = self.model.grid.get_cell_list_contents([position])
            if 'Wolf' in str(cell_contents):
                pass 
            else : 
                positions.append(position)
        
        if len(positions) > 0:
            position = self.random.choice(positions)
            self.model.grid.move_agent(self,position)
        else : 
            self.target_grass()


    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        proba = self.random.random() 
        if proba > 0.5: 
            self.target_grass()
        else : 
            self.avoid_wolves()
        # self.target_grass()
        self.energy -= 1
        self.reproduce()
        self.eat()
        self.check_if_alive()
        # ... to be completed
