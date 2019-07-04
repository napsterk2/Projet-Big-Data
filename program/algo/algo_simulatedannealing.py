from scipy import *
from matplotlib.pyplot import *

#Definition des paramètres

cities = 50
T0 = 15.0 #temperature initiale
Tmin = 0.01 #fixe la fin du recuit
tau = 10000 #définit la vitesse de baisse de température

#Fonction qui va permettre de calculer l'énergie totale, en mesurant la somme des distances entre les villes dans l'ordre de parcours du trajet, c'est à dire donc la distance de trajet.
def totalEnergy():
    global path
    energy = 0
    coordinates = c_[x[path],y[path]]
    print(coordinates)
    energy = sum(sqrt(sum((coordinates - roll(coordinates,-1,axis=0))**2,axis=1)))
    return energy

#Fonction qui va swapper un certain nombre de segments (entre i et j), ce qui entrainera un changement d'énergie dans le système
#Swap inverse lorsqu'elle est réappellé avec les mêmes valeurs (pour retour aux trajets antérieurs)
def swapping(i, j):
    global path
    Minimum = min(i,j)
    Maximum = max(i,j)
    path[Minimum:Maximum] = path[Minimum:Maximum].copy()[::-1]
    return

#Vérification de l'énergie, et on décide si la fluctuation est gardée ou non selon la proba de l'algo
def Metropolis(E1,E2):
    global T
    if E1 <= E2:
        E2 = E1  # énergie du nouvel état = énergie système
    else:
        dE = E1-E2
        if random.uniform() > exp(-dE/T): # la fluctuation est retenue avec la proba p. sinon retour trajet antérieur
            swapping(i,j)              
        else:
            E2 = E1 # la fluctuation est retenue 
    return E2

#variables à instancer
t = 0
T = T0

#variables d'historique
Henergy = []
Htime = []
Htemp = []

#timewindows
TWStart = []
TWStop = []

#Les coordonnées des villes (x,y) sont tirées aléatoirement selon la loi uniforme, x et y sont compris entre 0 et 1.
x = random.uniform(size=cities)
y = random.uniform(size=cities)

i = 0
while i < cities:
    TWStart.append(random.randint(0, 10))
    TWStop.append(random.randint(TWStart[i], TWStart[i]+100))
    i = i+1


#trajet initial réalisé selon l'ordre d'apparition des villes
path = arange(cities) ##créé un genre de tableau avec l'ordre des villes
initialPath = path.copy()

#On calcule la distance initiale séparant les villes, qu'il va falloir minimiser
Ec = totalEnergy()

while T>Tmin:
    #permet de choisir deux villes différentes au hasard
    i = random.randint(0, cities-1)
    j = random.randint(0, cities-1)
    if i == j: continue

    #On appelle le swapping et on mesure l'énergie
    swapping(i, j)
    Ef = totalEnergy()
    Ec = Metropolis(Ef, Ec)

    #loi de refroidissmenet
    t += 1
    T = T0*exp(-t/tau)

    #on rajoute les variables à l'historique
    if t % 10 == 0:
        Henergy.append(Ec)
        Htime.append(t)
        Htemp.append(T)

#display de nos resultats
print(float(Henergy[0]))
print(float(Ec))
print(float(t))


