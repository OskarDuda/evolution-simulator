from species_and_packs import *
from maps_and_tiles import *
from time import sleep
#from GUI import *
        
sp1 = Species('Xarz')
xarz = []
for i in range(60):
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
    xarz.append(Pack(sp1,id='',food=np.random.randint(3), pop=np.random.randint(30)+1, fur=np.random.randint(3), size=np.random.randint(15), aggressiveness=np.random.rand(),territory_size=np.random.randint(10), x=x_init, y=y_init, indicator='r^'))
    

sp2 = Species('Worgs')
worgs = []
for i in range(60):
    worgs.append(Pack(sp2,id='',food=np.random.randint(3), pop=np.random.randint(30)+1, fur=np.random.randint(3), size=np.random.randint(15), aggressiveness=np.random.rand(),territory_size=np.random.randint(10), x=int(np.random.rand()*M.x_size), y=int(np.random.rand()*M.y_size), indicator='yo'))
 
sp3 = Species('Muarx')
muarx = []
for i in range(60):
    muarx.append(Pack(sp3,id='',food=np.random.randint(3), pop=np.random.randint(30)+1, fur=np.random.randint(3), size=np.random.randint(15), aggressiveness=np.random.rand(),territory_size=np.random.randint(10), x=int(np.random.rand()*M.x_size), y=int(np.random.rand()*M.y_size), indicator='b*'))
 
#Choosing feature to plot
feature_to_plot = '' 
while not feature_to_plot.lower() in sp1.pack_attributes_names:
    feature_to_plot = input('What feature evolution do you want to follow? [type "features" for a list of features]: ')
    if feature_to_plot.lower() in ['features','f','feature']:
        print('Available features: ' + str(sp1.pack_attributes_names))
    elif not feature_to_plot.lower() in sp1.pack_attributes_names:
        print('Please choose a proper feature name.')

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
    
#create a vector containg changing values of fthe chosen feature
#for species in SPECIES_LIST:
#    for pack in species.packs_list:
#        tmp = 
#feature_vector = 
        

#window(100, 100, M.x_size, M.y_size, 'Map', M_temp)
    
v_statistics = []
n = 30
year = 0
fig = plt.figure()
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)
while(True):
    for day in range(n):
        M.generate_food()
        plt.subplot(211)
        ax1.title.set_text('Map')
        tmp = [] #vector of all packs' feature_to_plot values
        for species in SPECIES_LIST:
            for pack in species.packs_list:
                #pack lifecycle
                pack.cycle()
                
                #gather statistical data on all packs
                tmp.append(getattr(pack,feature_to_plot))
                
                plt.plot(pack.x, pack.y,pack.indicator) 
            species.count_survivors()
        
        plt.imshow(M_temp, cmap='Oranges', interpolation = 'nearest')
        v_statistics.append([max(tmp),np.median(tmp),min(tmp)])
        plt.subplot(212)
        ax2.title.set_text(feature_to_plot)
        plt.plot(v_statistics)
        plt.pause(0.01)
#        plt.close
        plt.clf()
        
#        ani = GUI.animation.FuncAnimation(fig, GUI.animate, interval=GUI.INTERVAL)
        
    for species in SPECIES_LIST:
        species.new_generation()
    print('Year {} ends'.format(year))
    if year < 1:
        v_statistics=[]
        
    year += 1
    
        
    

            