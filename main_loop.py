from species_and_packs import *
from maps_and_tiles import *
from time import sleep
#from GUI import *

        
sp1 = Species('Xarz')
xarz = []
for i in range(30):
    id=''
#    food=np.random.randint(3)
#    pop=np.random.randint(30)
#    fur=np.random.randint(3)
#    size=np.random.randint(15)
#    aggressiveness=np.random.rand()
#    territory_size=np.random.randint(10)
    x_init=int(np.random.rand()*M.x_size)
    y_init=int(np.random.rand()*M.y_size)
#    print('x:{},y:{}'.format(x,y))          
    xarz.append(Pack(sp1,id='',food=np.random.randint(3), pop=np.random.randint(30), fur=np.random.randint(3), size=np.random.randint(15), aggressiveness=np.random.rand(),territory_size=np.random.randint(10), x=x_init, y=y_init))
    

sp2 = Species('Worgs')
worgs = []
for i in range(30):
    worgs.append(Pack(sp2,id='',food=np.random.randint(3), pop=np.random.randint(30), fur=np.random.randint(3), size=np.random.randint(15), aggressiveness=np.random.rand(),territory_size=np.random.randint(10), x=int(np.random.rand()*M.x_size), y=int(np.random.rand()*M.y_size)))
 
sp3 = Species('Muarx')
muarx = []
for i in range(30):
    muarx.append(Pack(sp3,id='',food=np.random.randint(3), pop=np.random.randint(30), fur=np.random.randint(3), size=np.random.randint(15), aggressiveness=np.random.rand(),territory_size=np.random.randint(10), x=int(np.random.rand()*M.x_size), y=int(np.random.rand()*M.y_size)))
 

#draw the geography
M_temp = []
for i1 in M.tilemap:
    v = []
    for i2 in i1:
        v.append(i2.tile_type.temperature)
    M_temp.append(v)
 
#draw a point for each pack   
x_list = []
y_list = []
for species in SPECIES_LIST:
    for pack in species.packs_list:
        x_list.append(pack.x)
        y_list.append(pack.y)
    
fig = plt.plot(x_list,y_list,'g*')
fig = plt.imshow(M_temp, cmap='Oranges', interpolation = 'nearest')
#plt.pause(0.1)
plt.clf()

#window(100, 100, M.x_size, M.y_size, 'Map', M_temp)

n = 30
year = 0
while(True):
    for day in range(n):
        M.generate_food()
        x_list = []
        y_list = []
        for species in SPECIES_LIST:
            for pack in species.packs_list:
                x_list.append(pack.x)
                y_list.append(pack.y)
                pack.decide_movement()
                pack.get_hungry()
                pack.freeze()
                pack.eat()
#                print(type(worgs[0].population))
            
        
        fig = plt.plot(x_list,y_list,'g*')
        fig = plt.imshow(M_temp, cmap='Oranges', interpolation = 'nearest')
        plt.pause(0.01)
#        plt.close
        plt.clf()
        
#        ani = GUI.animation.FuncAnimation(fig, GUI.animate, interval=GUI.INTERVAL)
        
    for species in SPECIES_LIST:
        species.new_generation()
    print('Year {} ends'.format(year))
    year += 1
    
        
    

            