import numpy as np

def crossover(a0, a1, n=7):
    a0_modul = a0%n
    a1_modul = a1%n
    
    b0 = a0 - a0_modul + a1_modul
    b1 = a1 - a1_modul + a0_modul
    return ([b0,b1])

def mutation(a, dev):
    if hasattr(a,"__len__"):
        b=[]
        for k in a:
           b.append(np.random.normal(loc=k,scale=dev)) 
    else:
        b = np.random.normal(loc=a,scale=dev)
    
    return b
        
#def selection(v, )