import numpy as np
import genetic as gen
from maps_and_tiles import *

DICE = 15
VORES = ['Carnivore', 'Omnivore', 'Herbivore']
FUR = ['None','Short','Long']
CATEGORY_TRANSLATOR = {'fur':FUR,'food':VORES}
NOTIFICATIONS = False
BREEDING_PACE = 10
CROSS_BIG_CONST = 3 #crossover constant for attributes which can be higher than 1
CROSS_SMALL_CONST = 0.35 #has to be in range 0:1
HIGH_MUTATION_CONST = 0.07 #mutation chance for highly mutable attributes like size
LOW_MUTATION_CONST = 0.001 #mutation chance for lowly mutable attributes like type of food
SPECIES_LIST = []
FREEZE_TEMPS = [25,5,-5]
FREEZE_CHANCE = 0.03
TMP = 0 #variable for debugging
DEFAULT_PACK = { 'species':'Xarz', 
                'id':'', 'food':0, 
                'pop':1, 'fur':0, 
                'aggressiveness':0, 
                'satiety':0.0, 
                'size':1, 
                'territory_size':1, 
                'x':0, 
                'y':0, 
                'indicator':'g*'}

#Species groups packs with common genes
class Species:
    def __init__(self, name):
        self.name = name
        self.packs_list = []
        self.packs_id_list = [k.id for k in self.packs_list]
        self.generation = 1
        self.pack_attributes_names = self.make_pck_names()
        self.survivors = [p for p in self.packs_list if p.alive]
        SPECIES_LIST.append(self)
        
    def __repr__(self):
        return 'Species of {}, generation number {}, with {} representative groups'.format(self.name,self.generation,len(self.packs_list))
        
    
    def make_pck_names(self):
        tmp = Pack(self)
        self.packs_list.remove(tmp)
        return [a for a in dir(tmp) if (not a.startswith('__') and 
                               not callable(getattr(tmp,a)))]
    def count_survivors(self):
        self.survivors = [p for p in self.packs_list if p.alive]
        
    def new_generation(self):
        #selection (each pack that survived is selected once)        
        #crossover 
        d = {} #creating dictionary of all attribute values of all packs in the species - syntax is {'attr_name':[pack1.value,pack2_value,...],...}
        for attr in self.pack_attributes_names:
              d[attr] = []
        for pck in self.survivors:
            for attr in self.pack_attributes_names:
                d[attr].append(getattr(pck,attr))
            
        new_values = {} #creates a similar dictionary to d, with new attribute values
        if d['x']: #checks if any pack has survived
            for key in d:
                if key in ['alive', #these are attributes that are not modified through genetics
                           'food',
                           'food_intake',
                           'fur',
                           'id',
                           'satiety',
                           'species',
                           'x',
                           'y',
                           'indicator']: 
                    new_values[key] = d[key]
                elif type(d[key][0]) == int or (type(d[key][0]) == float and max(d[key]) >= 1): #these attributes can be higher than 1.0
                    new_values[key] = gen.vector_crossover(d[key],CROSS_BIG_CONST)
                elif type(d[key][0] == float): #these attributes are supposed to be from range 0:1
                    new_values[key] = gen.vector_crossover(d[key],CROSS_SMALL_CONST)
                else:
                    new_values[key] = d[key] #for bug avoidance all attributes not listed above stay unchanged in the crossover phase
        else: #if no pack has survived, generate a default pack
            for key in sp1.pack_attributes_names:
                new_values[key] = DEFAULT_PACK[key]
            
            
            
        #mutation
        for key in new_values:
            if new_values[key] in ['food','fur']:
                new_values[key] = gen.mutate_cat(new_values[key],LOW_MUTATION_CONST,CATEGORY_TRANSLATOR[key])
            elif new_values[key] in ['size','starting_population','territory_size']:
                new_values[key] = gen.mutate_int(new_values[key],HIGH_MUTATION_CONST)
            elif new_values[key] in ['aggressiveness']:
                new_values[key] = gen.mutate_float(new_values[key],HIGH_MUTATION_CONST)
        
                
        i = 0
        #new generation
        for pck in self.packs_list: #swaps attributes of old packs with new generation's attributes

#            print(len(new_values))
            for key in new_values:
                setattr(pck, key, new_values[key][i])
            i+=1
            i = i%len(self.survivors)
            #a little utillity
            pck.size = int(pck.size)
            if pck.size < 1:
                pck.size = 1
            pck.starting_population = int(pck.starting_population)
            if pck.starting_population < 1:
                pck.starting_population = 1
            pck.population = pck.starting_population
            
            
        self.generation += 1
        
#    def new_food(self, survivors):
#        food_translator = {'Carnivore':0, 'Omnivore':1, 'Herbivore':2}
#        v=[]
#        for s in survivors:
#            v.append(food_translator(s.food))
        
        
# A pack is a representative of a certain species    
class Pack:
    def __init__(self, sp, id='', food=0, pop=1, fur=0, aggressiveness=0, 
                 satiety=0.0, size=1, territory_size=1, x=0, y=0, 
                 indicator='g*'):
        self.species = sp #Species of animals in the pack
        if not id:
            self.id = sp.name+str(len(sp.packs_list)+1) #ID speaks for itself
        elif id in sp.packs_id_list:
            print('This ID is already in use! ')
            return
        else:
            self.id = id
        self.food = VORES[food] #Type of food the pack eats
        self.starting_population = int(pop) #Number of animals in the pack in the beginning
        self.population = self.starting_population #Number of animals in the pack
        self.fur = FUR[fur] #Fur length of animals in the pack
        if aggressiveness > 1.0:
            self.aggressiveness = 1.0 #0% - 100% chance of attacking those entering this pack's territory
        elif aggressiveness < 0.0:
                self.aggressiveness = 0.0
        else:
            self.aggressiveness = aggressiveness
        
        self.satiety = satiety #How full are the packs members' stomachs
        
        if size >= 1:
            self.size = size #How big are the animals in the pack
        else:
            self.size = 1
            
        self.territory_size = territory_size #How big area does the pack perceive as its own
        
        #X location of the pack
        if x > M.x_size: 
            self.x = M.x_size
        else:
            self.x = x
        #Y location of the pack
        if y > M.y_size: 
            self.y = M.y_size
        else:
            self.y = y
            
        self.food_intake = 0 #How much food does the whole pack need to survive
        self.count_food_intake()
        self.alive = True #Tells if the pack is alive
        M.tilemap[self.x][self.y].packs.append(self)
        self.indicator=indicator
        
        sp.packs_list.append(self)
    
    def __repr__(self):
        return 'A pack of {} {}, at x:{} y:{}, generation:{}'.format(self.population,self.species.name,self.x,self.y,self.species.generation)
    
    def cycle(self):
        self.decide_movement()
        self.get_hungry()
        self.freeze()
        self.eat()
    
    def move(self, dx, dy):
        if self.x+dx>=0  and self.x+dx<M.x_size and self.y+dy>=0 and self.y+dy<M.y_size:
            if self in M.tilemap[self.x][self.y].packs:
                M.tilemap[self.x][self.y].packs.remove(self)
            self.x += dx
            self.y += dy
            M.tilemap[self.x][self.y].packs.append(self)
            for xx in range(max(self.x-int(self.territory_size/2),0),min(self.x+int(self.territory_size/2),M.x_size)):
                for yy in range(max(self.y-int(self.territory_size/2),0),min(self.y+int(self.territory_size/2),M.y_size)):
                    for pack in M.tilemap[xx][yy].packs:
                        self.fight_or_flight(pack,NOTIFICATIONS)
        else:
            pass
    
    def decide_movement(self):
#        r = self.territory_size
#        tmp = [list(range(-r:r+1)+self.x*np.ones(d)),list(range(-r:r+1)+self.y*np.ones(d))]
#        max_food = max(np.array(M.tilemap)[np.ix_(tmp)])
        if self.alive:
            self.move(np.random.randint(5)-2,np.random.randint(5)-2)
                    
    def fight(self, p, print_output=False):
        self_throws = np.random.randint(DICE, size = self.population*int(self.size))
        defenders_throws = np.random.randint(DICE, size = int(p.population*p.size))
        
        dp = len(defenders_throws[defenders_throws == DICE - 1])
        if print_output:
            print('Group {} lost {} members'.format(self.id,dp ))
        self.change_population(-dp)

        
        dp = len(self_throws[self_throws == DICE - 1])
        if print_output:
            print('Group {} lost {} members'.format(p.id,dp ))
        p.change_population(-dp)
        
    def fight_or_flight(self, pack, print_output=False):
        decision_throw = np.random.rand()
        if self.aggressiveness == 0.0:
            pass
        elif decision_throw <= self.aggressiveness:
            if print_output:
                print('Group {} attacks group {}'.format(self.id, pack.id))
            self.fight(pack,NOTIFICATIONS)
        elif print_output:
            print('Groups go in opposite directions')
       
    def freeze(self):
        temperature = M.tilemap[self.x][self.y].tile_type.temperature
        freeze_throw = np.random.rand(self.population)
        if self.fur == FUR[0] and temperature < FREEZE_TEMPS[0]:
            self.change_population(-sum(freeze_throw < FREEZE_CHANCE))
        if self.fur == FUR[1] and temperature < FREEZE_TEMPS[1]:
            self.change_population(-sum(freeze_throw < FREEZE_CHANCE))
        if self.fur == FUR[2] and temperature < FREEZE_TEMPS[2]:
            self.change_population(-sum(freeze_throw < FREEZE_CHANCE))
            
    def count_food_intake(self):
        fur_modifier = 1.0
        if self.fur == FUR[1]:
            fur_modifier = 1.1
        elif self.fur == FUR[2]:
            fur_modifier = 1.2
        self.food_intake = self.population*self.size*fur_modifier
        
    def change_population(self, dp):
        if self.alive:
            self.population += int(dp)
            if dp < 0:
                M.tilemap[self.x][self.y].meat += dp
            if self.population <= 0:
                self.population = 0
                self.die()
        
    def get_hungry(self):
        self.satiety -= self.food_intake
        if self.satiety < 0:
            self.change_population(-1)
            self.satiety = 0
            
    
    def eat(self):
        if self.food == VORES[0]:
            meat_eaten = min(self.food_intake,M.tilemap[self.x][self.y].meat)
            eaten = meat_eaten
        elif self.food == VORES[1]:
            plants_eaten = min(self.food_intake,M.tilemap[self.x][self.y].plants)
            M.tilemap[self.x][self.y].plants -= plants_eaten
            if plants_eaten < self.food_intake:
                meat_eaten = min(self.food_intake-plants_eaten,M.tilemap[self.x][self.y].meat)
                M.tilemap[self.x][self.y].meat -= meat_eaten
                eaten = plants_eaten+meat_eaten
            else:
                eaten = plants_eaten
        elif self.food == VORES[2]:
            plants_eaten = M.tilemap[self.x][self.y].plants
            M.tilemap[self.x][self.y].plants -= plants_eaten
            eaten = plants_eaten
        else:
            eaten = 0
        self.satiety += eaten
        
    
    def die(self):
        if NOTIFICATIONS:
            print('Pack {} died'.format(self.id))
        M.tilemap[self.x][self.y].meat += self.starting_population
        self.indicator = 'k+'
        self.alive = False
         
#sp1 = Species('dogs')
#p11 = Pack(sp1, id='', food=0, pop=5, fur=2, size=4, aggressiveness=0.6, satiety=0)
#p12 = Pack(sp1, id='', food=0, pop=3, fur=1, size=5, aggressiveness=0.7, satiety=0)
#p13 = Pack(sp1, id='', food=0, pop=3, fur=2, size=7, aggressiveness=0.9, satiety=0)
#
#sp2 = Species('cats')
#p21 = Pack(sp2, food=0, pop=9, fur=1, size=3, aggressiveness=0.7, satiety=0)
#
#print('p1 group size:{}, p2 group size: {}'.format(p11.population, p21.population))
#p11.fight_or_flight(p21,print_output=True)
#print('p1 group size:{}, p2 group size: {}'.format(p11.population, p21.population))
#
#survivors = [p for p in sp1.packs_list if p.alive]
#        #crossover 
#d = {}
##        f_int = lambda a, p:d[a].append(getattr(p,a))
#for attr in sp1.pack_attributes_names:
#              d[attr] = []
#for pck in sp1.packs_list:
#            for attr in sp1.pack_attributes_names:
#                d[attr].append(getattr(pck,attr))
                