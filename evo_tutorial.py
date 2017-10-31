SELECTOR = {'overall':tutor_overall,
            'species':tutor_packs_and_species,
            'maps':tutor_maps,
            'genetic':tutor_genetic,
            'quit':quit_tutorial}
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
              '1':'species',
              '2':'maps',
              '3':'genetic'}
   
def tutor_overall():
    print('\n\nThis application simulates live of simple animal groups called "packs". '+
          'These packs move around their environment trying to gather food to survive. '+
          'Packs get hungry, can freeze to death and also can attack each other. '+
          'After a set amount of time a new generation is created in place of the old packs. '+
          'Genetic algorithms are involved in the process of creation of the new generation. '+
          'More specific information is included in the specific  tutorials.')
    return True
    
def tutor_packs_and_species():
    print('Animals are grouped in packs which are logically the smallest objects in the application. '+
          'Packs are grouped into species. Just like in nature animals can cross their genes inside their own species. '+
          'Packs class attributes include population of the pack, type of food given pack eats (meat,plants or both), '+
          'animals size, fur length, aggressiveness and territory size. ' +
          '')
    return True
    
def tutor_maps():
    return True
    
def tutor_genetic():
    return True

def quit_tutorial():
    return False

def tutor_main(contin=True):
    print('This application simulates evoulution of species in a closed environment.'+
                    'It consists of three main elements:')
    while contin:
        sel = input('1. Animals grouped in packs [type "species" for more]\n'+
                    '2. The environment in which the packs operate [type "maps" for more]\n'+
                    '3. The genetics of the animals [type "genetic" for more]\n'+
                    'For an overall description of the system type "overall"\n'+
                    'If you want to quit the tutorial type "quit"\n')
        contin = SELECTOR[TRANSLATOR[sel.lower()]]()
        
     
tutor_main()