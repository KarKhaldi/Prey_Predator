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
        self.grown = fully_grown
        self.initial_countdown = countdown
        self.countdown = countdown
        self.pos = pos




    def step(self):
        """ 
        function that deals with the state of the grass patch
        """
        if self.grown == True :
            pass
        # if the countdown is 0 the dead grass can be changed into a green one (grown one)
        elif self.countdown == 0:
            self.grown = True
            self.countdown = self.initial_countdown
        # in the case where the grass is not fully grown, it will be removed from the model with a certain probability
        elif self.countdown > 0 :
            proba = self.random.random()
            if proba > 0.15:
                self.countdown -= 1
            else :
                self.model.where_are_grasses[self.pos] = 0
                self.model.schedule.remove(self)
                self.model.grid.remove_agent(self)

        


