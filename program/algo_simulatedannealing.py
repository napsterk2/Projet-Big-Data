from scipy import *
from matplotlib.pyplot import *

#Definition des paramètres

cities = 50
T0 = 10.0 #temperature initiale
Tmin = 0.01 #fixe la fin du recuit
tau = 10000 #définit la vitesse de baisse de température

#Fonction qui va permettre de calculer l'énergie totale, en mesurant la somme des distances entre les villes dans l'ordre de parcours du trajet
def totalEnergy():
    global path
    energy = 0
    coordinates = c_[x[path],y[path]]
    energy = sum(sqrt(sum((coordinates - roll(coordinates,-1,axis=0))**2,axis=1)))
    return energy

#Fonction qui va swapper un certain nombre de segments (entre i et j), ce qui entrainera un changement d'énergie dans le système
#Swap inverse lorsqu'elle est réappellé avec les mêmes valeurs (pour retour aux trajets antérieurs)
def swapping():
    global path
    Minimum = min(i,j)
    Maximum = max(i,j)
    path[Minimum:Maximum] = path[Minimum:Maximum].copy()[::-1]
    return

def Metropolis(E1,E2):
    global T
    if E1 <= E2:
        E2 = E1  # énergie du nouvel état = énergie système
    else:
        dE = E1-E2
        if random.uniform() > exp(-dE/T): # la fluctuation est retenue avec  
            Fluctuation(i,j)              # la proba p. sinon retour trajet antérieur
        else:
            E2 

#variables d'historique
Henergy = []
Htime = []
HTemp = []

#placement de N villes sur le plan
x = random.uniform(size=cities)
y = random.uniform(size=cities)

#trajet initial réalisé selon l'ordre d'apparition des villes

