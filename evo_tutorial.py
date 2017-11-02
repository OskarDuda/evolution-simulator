   
def tutor_overall():
    print('\n\nThis application simulates live of simple animal groups called "packs". '+
          'These packs move around their environment trying to gather food to survive. '+
          'Packs get hungry, can freeze to death and also can attack each other. '+
          'After a set amount of time a new generation is created in place of the old packs. '+
          'Genetic algorithms are involved in the process of creation of the new generation. '+
          'Simulation is divided into years after which a new generation of packs is created. '+
          'Each year is divided into n "turns" in which food is restored and animals move. ' +
          'More specific information is included in the specific  tutorials.\n')
    return True
    
def tutor_packs_and_species():
    print('Animals are grouped in packs which are logically the smallest objects in the application. '+
          'Packs are grouped into species. Just like in nature animals can cross their genes inside their own species. '+
          'Packs class attributes include population of the pack, type of food given pack eats (meat,plants or both), '+
          'animals size, fur length, aggressiveness and territory size.\n' +
          '')
    return True
    
def tutor_maps():
    print('The geography of the simulator is placed in a single variable M. ' +
          'It is an object of a map class, which is constructed of tiles. '+
          'Attributes of a tile include temperature, '+
          'food (meat and plants) available at given moment '+
          'and food produced in each "turn".\n')
    return True
    
def tutor_genetic():
    print('Every year in the simulation a new generation of packs is generated. '+
          'As always a genetic algorithm is divided into selection, crossover and mutation.\n'+
          '1. Selection - survival of a pack is the only condition for selection right now.\n'+
          '2. Crossover - crossover procedure is than conducted in pairs of selected packs.\n'+
          '3. Mutation - there is a seperate chance of mutation for percentage floats, regular floats, '+
          'integegers and categorial attributes.\n'+
          'Floats have a given chance of being increased by a random (positive or negative) normally distributed value.\n '+
          'Integers have a given chance of being increase or decreased by 1\n'+
          'Categorical attributes have a very small chance of being changed into another value from the given category.\n\n'+
          'After the above three steps a new population is created which is as numerous '+
          'as the initial population of the whole simulation.\n') 
    return True

def tutor_visualization():
    print('The user chooses which attribute of the animals they want to follow. '+
          'The highest value, the median and the lowest value of the attribute within the whole present population '+
          'are than plotted and refreshed after each year (each new generation).\n')

def quit_tutorial():
    return False

def tutor_main(contin=True):
    print('This application simulates evoulution of species in a closed environment.'+
          'It consists of three main elements and the visualization process:')
    while contin:
        sel = input('1. Animals grouped in packs [type "species" for more]\n'+
                    '2. The environment in which the packs operate [type "maps" for more]\n'+
                    '3. The genetics of the animals [type "genetic" for more]\n'+
                    'To learn more about visualization provided type "visualization"\n'+
                    'For an overall description of the system type "overall"\n'+
                    'If you want to quit the tutorial type "quit"\n')
        contin = SELECTOR[TRANSLATOR[sel.lower()]]()


SELECTOR = {'overall':tutor_overall,
            'species':tutor_packs_and_species,
            'maps':tutor_maps,
            'genetic':tutor_genetic,
            'quit':quit_tutorial,
            'visualization':tutor_visualization}
#            'o':SELECTOR['overall'], #FOR LATER IMPLEMENTATION
#            'over':SELECTOR['overall'],
#            'gen':SELECTOR['genetic'],
#            'g':SELECTOR['genetic'],
#            's':SELECTOR['species'],
#            'sp':SELECTOR['species'],
#            'm':SELECTOR['maps'],
#            'q':SELECTOR['quit']}
TRANSLATOR = {'overall':'overall',
              'species':'species',
              'maps':'maps',
              'genetic':'genetic',
              'visualization':'visualization',
              'quit':'quit',
              'o':'overall',
              'over':'overall',
              'gen':'genetic',
              'g':'genetic',
              's':'species',
              'sp':'species',
              'm':'maps',
              'map':'maps',
              'q':'quit',
              'vis':'visualization',
              'v':'visualization',
              'visual':'visualization',
              '1':'species',
              '2':'maps',
              '3':'genetic',
              '4':'visualization',
              '5':'overall',
              '6':'quit'}        
     