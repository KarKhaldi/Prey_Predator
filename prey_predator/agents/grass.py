from mesa import Agent
from prey_predator.random_walk import RandomWalker



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

        


