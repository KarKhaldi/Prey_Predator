from mesa import Agent
from prey_predator.random_walk import RandomWalker
from prey_predator.agents.grass import GrassPatch
# from prey_predator.agents.wolf import Wolf



class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.pos = pos
    
    def check_if_alive(self):
        """
        if the sheep has no more energy, he gets removed from the modelisation 
        """
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
        """  
        If the sheep is on a grass patch, it eats it and gains energy
        """

        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_contents:
            if isinstance(agent,GrassPatch) and agent.grown :
                self.energy += self.model.sheep_gain_from_food 
                agent.grown = False
                break

    def reproduce(self):
        """ 
        if the sheep has enough energy, it reproduces and shares its energy with its child
        """

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
        """ 
        The sheep target the grass patches in its neighborhood and move towards it
        """

        # we will list all the possible positions and then choose one of them
        positions = []
        # we get the neighborhood of the sheep
        possible_positions = self.model.grid.get_neighborhood( self.pos, moore=True, include_center=False)
        # we check if there is a grass patch in the neighborhood
        for position in possible_positions:
            cell_contents = self.model.grid.get_cell_list_contents([position])
            for agent in cell_contents:
                if isinstance(agent,GrassPatch) and agent.grown:
                    positions.append(position)
                    break
        
        # if grass patches were found, we choose one of them randomly
        if len(positions) > 0:
            position = self.random.choice(positions)
        else : 
            # if no grass patch was found, we choose a random position in the neighborhood
            position = self.random.choice(possible_positions)

        self.model.grid.move_agent(self,position)
    
    def avoid_wolves(self):
        """
        The sheep tries to avoid the wolves in its neighborhood
        """

        positions = []
        possible_positions = self.model.grid.get_neighborhood( self.pos, moore=True, include_center=False)
        for position in possible_positions:
            cell_contents = self.model.grid.get_cell_list_contents([position])
            ## if there is a wolf in the neighborhood, we don't add the position to the list
            if 'Wolf' in str(cell_contents):
                pass 
            else : 
                positions.append(position)
        ## we only have left the positions that do not have a wolf on 
        if len(positions) > 0:
            position = self.random.choice(positions)
            self.model.grid.move_agent(self,position)
        else : 
            self.target_grass()


    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        ## we choose randomly if the sheep will target the grass or avoid the wolves
        proba = self.random.random() 
        if proba > 0.5: 
            self.target_grass()
        else : 
            self.avoid_wolves()
        self.energy -= 1
        self.reproduce()
        self.eat()
        self.check_if_alive()
