from mesa import Agent
from prey_predator.random_walk import RandomWalker


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

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        self.energy -= 1
        self.reproduce()
        self.eat()
        self.check_if_alive()
        # ... to be completed


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


    def eat(self):
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_contents:
            if isinstance(agent,Sheep) :
                self.energy += self.model.wolf_gain_from_food
                self.model.schedule.remove(agent)
                self.model.grid.remove_agent(agent)
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
        # ... to be completed


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        # ... to be completed
        self.grown = fully_grown
        self.initial_countdown = countdown
        self.countdown = countdown
        self.pos = pos




    def step(self):
        # ... to be completed    
        if self.grown == True :
            pass
        elif self.countdown == 0:
            self.grown = True
            self.countdown = self.initial_countdown
        elif self.countdown > 0 :
            proba = self.random.random()
            if proba > 0.15:
                self.countdown -= 1
            else :
                self.model.where_are_grasses[self.pos] = 0
                self.model.schedule.remove(self)
                self.model.grid.remove_agent(self)

        