import numpy as np

DICE = 20
VORES = ['Carnivore', 'Omnivore', 'Herbivore']
FUR = ['None','Short','Long']
NOTIFICATIONS = True

class Species:
    def __init__(self, name):
        self.name = name
        self.packs_list = []
        
    

class Pack:
    def __init__(self, sp, id='', food=0, pop=1, fur=0, aggressiveness=0, satiety=0.0, size=1, territory_size=1, x=0, y=0):
        self.species = sp #Species of animals in the pack
        if not id:
            self.id = sp.name+str(len(sp.packs_list)+1) #ID speaks for itself
        else:
            self.id = id
        self.food = VORES[food] #Type of food the pack eats
            
        self.population = pop #Number of animals in the pack
        self.fur = FUR[fur] #Fur length of animals in the pack
        if aggressiveness > 1.0:
            self.aggressiveness = 1.0 #0% - 100% chance of attacking those entering this pack's territory
        elif aggressiveness < 0.0:
                self.aggressiveness = 0.0
        else:
            self.aggressiveness = aggressiveness
        
        self.satiety = satiety #How full are the packs members stomachs
        self.size = size #How big are the animals in the pack
        self.territory_size = territory_size #How big area do the pack perceives as its own
        self.x = x #X location of the pack
        self.y = y #Y location of the pack
        self.food_intake = 0 #How much food does the whole pack need to survive
        self.count_food_intake()
        self.dead = False #Tells if the pack is dead
        
        sp.packs_list.append(self)
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
    def fight(self, p, print_output=False):
        self_throws = np.random.randint(DICE, size = self.population*self.size)
        defenders_throws = np.random.randint(DICE, size = p.population*p.size)
        
        dp = len(defenders_throws[defenders_throws == DICE - 1])
        if print_output:
            print('Group {} lost {} members'.format(self.id,dp ))
        self.change_population(-dp)

        
        dp = len(self_throws[self_throws == DICE - 1])
        if print_output:
            print('Group {} lost {} members'.format(p.id,dp ))
        p.change_population(-dp)
       
    
    def fight_or_flight(self, p, print_output=False):
        decision_throw = np.random.rand()
        if self.aggressiveness == 0.0:
            pass
        elif decision_throw <= self.aggressiveness:
            if print_output:
                print('Group {} attacks group {}'.format(self.id, p.id))
            self.fight(p,NOTIFICATIONS)
        elif print_output:
            print('Groups go in opposite directions')
            
    def count_food_intake(self):
        fur_modifier = 1.0
        if self.fur == FUR[1]:
            fur_modifier = 1.1
        elif self.fur == FUR[2]:
            fur_modifier = 1.2
        self.food_intake = self.population*self.size*fur_modifier
        
    def change_population(self, dp):
        if not self.dead:
            self.population += dp
            if self.population <= 0:
                self.population = 0
                self.die()
        
    def count_satiety(self):
        self.satiety -= self.food_intake
        if self.satiety > self.population:
            self.change_population(-1)
            self.satiety = self.population
        if 2*self.satiety < self.population:
            self.change_population(self.population)
            self.satiety = self.population
            
    
    def die(self):
        self.dead = True
        print('Pack {} died'.format(self.id))
         
        
sp1 = Species('dogs')
p1 = Pack(sp1, id='', food=0, pop=5, fur=2, size=4, aggressiveness=0.6, satiety=0)

sp2 = Species('cats')
p2 = Pack(sp2, food=0, pop=9, fur=1, size=3, aggressiveness=0.7, satiety=0)

print('p1 group size:{}, p2 group size: {}'.format(p1.population, p2.population))
p1.fight_or_flight(p2,print_output=True)
print('p1 group size:{}, p2 group size: {}'.format(p1.population, p2.population))