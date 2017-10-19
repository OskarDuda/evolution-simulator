import numpy as np
import genetic as gen

DICE = 20
VORES = ['Carnivore', 'Omnivore', 'Herbivore']
FUR = ['None','Short','Long']
CATEGORY_TRANSLATOR = {'fur':FUR,'food':VORES}
NOTIFICATIONS = True
BREEDING_PACE = 5
CROSS_BIG_CONST = 3
CROSS_SMALL_CONST = 0.35 #has to be in range 0:1
HIGH_MUTATION_CONST = 0.1 #mutation chance for highly mutable attributes like size
LOW_MUTATION_CONST = 0.001 #mutation chance for lowly mutable attributes like type of food
SPECIES_LIST = []
FREEZE_TEMPS = [25,5,-5]
FREEZE_CHANCE = 0.3

class Species:
    def __init__(self, name):
        self.name = name
        self.packs_list = []
        self.generation = 1
        self.pack_attributes_names = self.make_pck_names()
        SPECIES_LIST.append(self)
        
    def __repr__(self):
        return 'Species of {}, generation number {}, with {} representatives'.format(self.name,self.generation,len(self.packs_list))
        
    
    def make_pck_names(self):
        tmp = Pack(self)
        self.packs_list.remove(tmp)
        return [a for a in dir(tmp) if (not a.startswith('__') and not callable(getattr(tmp,a)))]
        
        
    def new_generation(self):
        #selection (each pack that survived is selected once)
        survivors = [p for p in self.packs_list if p.alive]
        
        #crossover 
        def f_big(v): #function for crossover of attributes that can get higher than 1.0
            i = 0
            r = np.zeros(len(v))
            while i < len(v):
                tmp = gen.crossover(v[i-1],v[i],CROSS_BIG_CONST)
                r[i-1] = tmp[0]
                r[i] = tmp[1]
                i += 1
            return list(r)
        
        def f_small(v): #function for crossover of attributes from range 0:1
            i = 0
            r = []
            while i < len(v):
                tmp = gen.crossover(v[i-1],v[i],CROSS_SMALL_CONST)
                r[i-1] = tmp[0]
                r[i] = tmp[1]
            return r
        
        d = {} #creating dictionary of all attribute values of all packs in the species - syntax is {'attr_name':[pack1.value,pack2_value,...],...}
        for attr in self.pack_attributes_names:
              d[attr] = []
        for pck in survivors:
            for attr in self.pack_attributes_names:
                d[attr].append(getattr(pck,attr))
        
        new_values = {} #creates a similar dictionary to d, with new attribute values
        for key in d:
            if key in ['alive' , 'food', 'food_intake', 'fur', 'id', 'satiety', 'species', 'x', 'y']: #these are attributes that are not passed through genetics
                new_values[key] = d[key]
            elif type(d[key][0]) == int or (type(d[key][0]) == float and max(d[key]) >= 1): #these attributes can be higher than 1.0
                new_values[key] = f_big(d[key])
            elif type(d[key][0] == float): #these attributes are supposed to be from range 0:1
                new_values[key] = f_small(d[key])
            else:
                new_values[key] = d[key] #for bug avoidance all attributes not listed above stay unchanged in the crossover phase
            
        #mutation
        def mut_float(a, dev): #returns gaussian distribution of values with std deviation equal to dev, concentrated around value from a
            return gen.mutation(a, dev)
        
        def mut_int(a,chance): #changes values in a by 1 with possibility equal to chance
            if hasattr(a,'__len__'):
                n = len(a)
                sgn = np.random.randint(2,size=n)
                sgn = [2*x-1 for x in sgn]
                decider = np.random.rand(n)<chance
                b = np.array(a)
                b[decider] += sgn[decider]
                return list(b)
            else:
                n = 1
                sgn = np.random.randint(2)
                sgn = 2*sgn - 1
                b = a
                if np.random.rand()<chance:
                    b = a + sgn
            
            
            
        def mut_cat(a,chance,category): #changes values in a into neighbouring value from category
            
            if hasattr(a,'__len__'):
                n = len(a)
                sgn = np.random.randint(2,size=n)
                sgn = [2*x-1 for x in sgn]
                decider = np.random.rand(n) < chance
                for i in range(n):
                    if decider[i]:
                        b[i]=category[category.index(a[i])+sgn[i]]
                return list(b)
            else:
                if np.random.rand() < chance:
                    sgn = 2*np.random.randint(2)-1
                    b = category[category.index(a)+sgn]
                return b
                    
        for key in new_values:
            if new_values[key] in ['food','fur']:
                new_values[key] = mut_cat(new_values[key],LOW_MUTATION_CONST,CATEGORY_TRANSLATOR[key])
            elif new_values[key] in ['size','starting_population','territory_size']:
                new_values[key] = mut_int(new_values[key],HIGH_MUTATION_CONST)
            elif new_values[key] in ['aggressiveness']:
                new_values[key] = mut_float(new_values[key],HIGH_MUTATION_CONST)
        
        
        #new generation
        i = 0            
        for pck in self.packs_list: #swaps attributes of old packs with new generation's attributes
            for key in new_values:
                setattr(pck, key, new_values[key][i])
            i+=1
            pck.population = pck.starting_population
            
        self.generation += 1
        
    def new_food(self, survivors):
        food_translator = {'Carnivore':0, 'Omnivore':1, 'Herbivore':2}
        v=[]
        for s in survivors:
            v.append(food_translator(s.food))
        
        
    
class Pack:
    def __init__(self, sp, id='', food=0, pop=1, fur=0, aggressiveness=0, satiety=0.0, size=1, territory_size=1, x=0, y=0):
        self.species = sp #Species of animals in the pack
        if not id:
            self.id = sp.name+str(len(sp.packs_list)+1) #ID speaks for itself
        else:
            self.id = id
        self.food = VORES[food] #Type of food the pack eats
        self.starting_population = pop #Number of animals in the pack in the beginning
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
        self.alive = True #Tells if the pack is alive
        
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
       
    def freeze(self, temperature):
        freeze_throw = np.random.rand(self.population)
        if self.fur == FUR[0] and temperature < FREEZE_TEMPS[0]:
            self.change_population(-sum(freeze_throw < FREEZE_CHANCE))
        if self.fur == FUR[1] and temperature < FREEZE_TEMPS[1]:
            self.change_population(-sum(freeze_throw < FREEZE_CHANCE))
        if self.fur == FUR[2] and temperature < FREEZE_TEMPS[2]:
            self.change_population(-sum(freeze_throw < FREEZE_CHANCE))
            
    
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
        if not self.alive:
            self.population += dp
            if self.population <= 0:
                self.population = 0
                self.die()
        
    def get_hungry(self):
        self.satiety -= self.food_intake
        if self.satiety < 0:
            self.change_population(-1)
            self.satiety = 0
            
    
    def eat(self, amount):
        self.satiety += amount
        if self.satiety > BREEDING_PACE*self.size:
            self.population += 1
            self.satiety = BREEDING_PACE*self.size
    
    def die(self):
        self.alive = False
        M.tilemap()
        print('Pack {} died'.format(self.id))
         
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
                