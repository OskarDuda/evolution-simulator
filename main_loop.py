from species_and_packs import *
from maps_and_tiles import *

        
sp1 = Species('Xarz')
xarz = []
for i in range(10):
    xarz.append(Pack(sp1,id='',food=np.random.randint(3), pop=np.random.randint(30), fur=np.random.randint(3), size=np.random.randint(15), aggressiveness=np.random.rand(),territory_size=np.random.randint(10)))
    

sp2 = Species('Worgs')
worgs = []
for i in range(10):
    worgs.append(Pack(sp1,id='',food=np.random.randint(3), pop=np.random.randint(30), fur=np.random.randint(3), size=np.random.randint(15), aggressiveness=np.random.rand(),territory_size=np.random.randint(10)))
 
sp3 = Species('Muarx')
muarx = []
for i in range(10):
    muarx.append(Pack(sp1,id='',food=np.random.randint(3), pop=np.random.randint(30), fur=np.random.randint(3), size=np.random.randint(15), aggressiveness=np.random.rand(),territory_size=np.random.randint(10)))
 

M = Map(300,150,geographic_tilemap_generator_by_temp)
M_temp = []
for i1 in M.tilemap:
    v = []
    for i2 in i1:
        v.append(i2.tile_type.temperature)
    M_temp.append(v)
plt.imshow(M_temp, cmap='Oranges', interpolation = 'nearest')
plt.show()

