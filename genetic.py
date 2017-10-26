import numpy as np

def crossover(a0, a1, n=7):
    a0_modul = a0%n
    a1_modul = a1%n
    
    b0 = a0 - a0_modul + a1_modul
    b1 = a1 - a1_modul + a0_modul
    return ([b0,b1])
        
def vector_crossover(v,n=7):
    r = np.zeros(len(v))
    if len(v)%2 == 0:
        for i in range(len(v)):
             if i%2 == 0:
                 r[i] = crossover(v[i],v[i+1],n)[0]
                 r[i+1] = crossover(v[i],v[i+1],n)[1]
    else:
         for i in range(len(v)-1):
             if i%2 == 0:
                 r[i] = crossover(v[i],v[i+1],n)[0]
                 r[i+1] = crossover(v[i],v[i+1],n)[1]  
         r[-1]=crossover(v[0],v[-1],n)[1]
    return r

def mutate_float(a, dev):
    if hasattr(a,"__len__"):
        b=[]
        for k in a:
           b.append(np.random.normal(loc=k,scale=dev)) 
    else:
        b = np.random.normal(loc=a,scale=dev)
    
    return b

def mutate_int(a,chance): #changes values in a by 1 with possibility equal to chance
    if hasattr(a,'__len__'):
        n = len(a)
        sgn = np.random.randint(2,size=n) #decides whether a changing value will increase or decrease
        sgn = [2*x-1 for x in sgn]
        decider = np.array(np.random.rand(n)<chance) #decides which values will change
        b = np.array(a)
        b[decider] += np.array(sgn)[decider]
        return list(b)
    else:
        if np.random.rand()<chance:
            return a + 2*np.random.randint(2) - 1
        else:
            return a
        
def mutate_cat(a,chance,category): #changes values in a into neighbouring value from category
    if hasattr(a,'__len__') and not type(a)==str:
        n = len(a)
        sgn = np.random.randint(2,size=n) #decided whether changing values will go left or right
        sgn = [2*x-1 for x in sgn]
        decider = np.random.rand(n) < chance #decides which values will change
        b=np.array(a)
        for i in range(n):
            if decider[i]:
                b[i]=category[category.index(a[i])+sgn[i]]
        return list(b)
    else:
        if np.random.rand() < chance:
            return category[category.index(a)+2*np.random.randint(2)-1]
        else:
            return a

#def selection FOR LATER IMPLEMENTATION