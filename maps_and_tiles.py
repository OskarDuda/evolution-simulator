import numpy as np
import matplotlib.pyplot as plt

TILE_TYPES = []
class Tile_type:
    def __init__(self, id='', plants_inc=0.0, meat_inc=0.0, temperature=0.0):
        if not id:
            self.id = 'Custom_Tile'+str(len(TILE_TYPES)+1) #ID speaks for itself
        else:
            self.id = id
        self.plants_income = plants_inc #How fast plants grow on this tile type
        self.meat_income = meat_inc #How much meat is regurarly generated on this tile type
        self.temperature = temperature #Temperature of the tile type affects animals living here
        TILE_TYPES.append(self)
    
class Tile:
    def __init__(self, tt=Tile_type(), plants=0.0, meat=0.0,x=0,y=0, ):
        self.tile_type = tt
        self.plants = plants
        self.meat = meat
        self.x = x
        self.y = y
        self.packs = []
    def __repr__(self):
        return 'A tile of {}, with {} edible plants and {} meat'.format(self.tile_type.id,self.plants,self.meat)
        
class Map:
    def __init__(self,x_size,y_size,f):
        self.x_size = x_size
        self.y_size = y_size
        self.tilemap = self.generate_tilemap(x_size, y_size,f)
        
        
        
    def generate_tilemap(self, x_size, y_size, f):
        return f(x_size, y_size)
    
    def generate_food(self):
        for mx in self.tilemap:
            for m in mx:
                m.plants += m.tile_type.plants_income
                m.meat += m.tile_type.meat_income
    

def geographic_tilemap_generator_by_temp(x_size, y_size):
    a = []
    for t in TILE_TYPES:
        a.append(t.temperature) 
    base = 1.1 
    step = (max(a)-min(a))/y_size
    r =[]
    i = max(a)
    tmp = []
    for i1 in range(x_size):
        a_roul = np.cumsum(a)*((1/base) ** (np.square((np.array(a) - i*np.ones(len(a))))))
        v = []
        for i2 in range(y_size):
            ran = np.random.rand()
            indic = sum(a_roul > ran)-1
            v.append(Tile(tt=TILE_TYPES[indic],x=i1,y=i2))
        r.append(v)
        tmp.append(i)
        i -= step
    return r

t1 = Tile_type(id='desert',temperature=40.0)
t1 = Tile_type(id='jungle', plants_inc=0.4, meat_inc=0.2, temperature=35.0)
t1 = Tile_type(id='mountains', plants_inc=0.2, temperature=10.0)
t1 = Tile_type(id='taiga', plants_inc=0.3, meat_inc=0.1, temperature=10.0)
t1 = Tile_type(id='woodlands', plants_inc=0.2, meat_inc=0.1, temperature=20.0)
t1 = Tile_type(id='lakeside', plants_inc=0.2, meat_inc=0.1, temperature=20.0)
t1 = Tile_type(id='meadows', plants_inc=0.3, meat_inc=0.1, temperature=25.0)
t1 = Tile_type(id='polar', temperature=-10.0)
t1 = Tile_type(id='tundra', plants_inc=0.1, temperature=-10.0)

M = Map(50,50,geographic_tilemap_generator_by_temp)