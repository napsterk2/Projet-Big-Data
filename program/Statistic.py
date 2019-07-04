from typing import List, Any
import random
from program.report import AlgoResult
from program.run import run_tabu_search_multistart
import statistics
#from program.utilities import *
from mongoengine import connect
from program.report import *

from statistics import mean


def temps_exec_cities(result):
    results = result
    listTempsExec = []
    for i in results:
        listTempsExec.append(i.exec_time)
    tempsExecMoyen = mean(listTempsExec)
    print("Pour ", results[0].nbr_cities, "villes le temps d'éxécution moyenne est de ", tempsExecMoyen, " secondes")
    return tempsExecMoyen

def ram_cities(result):
    results = result
    listRam = []
    for i in results:
        listRam.append(i.avg_ram_usage)
    ramMoyen = mean(listRam)
    print("Pour ", results[0].nbr_cities, "villes l'usage moyen de la RAM est de ", ramMoyen, " méga")
    return ramMoyen

def temps_exec_itteration(result):
    results = result
    listExecItteration = []
    for i in results:
        listExecItteration.append(i.exec_time / i.iter_nb)
    tempsExecVillesMoyen = mean(listExecItteration)
    print("Le temps moyen d'éxécution pour une ittération est de " ,tempsExecVillesMoyen, " secondes")
    return tempsExecVillesMoyen

def moyenne_distances(result):
    results = result
    listDistance = []
    for i in results:
        for u in i.adjacency_matrix:
            for x in u:
                listDistance.append(x)
    distanceMoyenneVille = mean(listDistance)
    print("La distance moyenne entre deux villes est de " ,distanceMoyenneVille, " en ayant une distance maximal de" ,results[0].max_city_distance, "entre chaque ville")

def ecart_optimum_local(result):
    results = result
    listMissmatch = []
    listJourneyDuration = []
    listPathLen = []
    for i in results:
        for u in i.local_optimum_value_history:
            listJourneyDuration.append(u["journey_duration"])
            listMissmatch.append(u["del_missmatch"])
            listPathLen.append(u["path_len"])
    trieListJourneyDuration = sorted(listJourneyDuration)
    trieListMissmatch = sorted(listMissmatch)
    trieListPathLen = sorted(listPathLen)
    ecartJourneyDuration = (trieListJourneyDuration[-1] - trieListJourneyDuration[0])
    ecartMissmatch = (trieListMissmatch[-1] - trieListMissmatch[0])
    ecartPathLen = (trieListPathLen[-1] - trieListPathLen[0])

    print("L'écart entre la longeur de chemin parcouru la plus longue et la plus courte trouvé est de ", ecartPathLen,)
    print("L'écart entre le temps d'attente le plus long et le plus court est de " , ecartMissmatch,)
    print("L'écart entre la durée de trajet la plus longue et la plus courte est de ", ecartJourneyDuration,)

def écart_temps_parours_missmatch_ecart_max_villes_obj_plus_tard(result):
    results = result
    listDureeparcours = []
    listMissmatch = []
    for i in results:
        listDureeparcours.append(i.global_opt_journey_duration)
        listMissmatch.append((i.global_opt_win_missmatch))
    meanDureeParcours = mean(listDureeparcours)
    meanMissmatch = mean(listMissmatch)
    écartDureeParcoursMissmatch = abs((meanDureeParcours - meanMissmatch))
    print("l'écart moyen entre la durée du parcours et le manque de temps de livraison est de ", écartDureeParcoursMissmatch, " avec un maximum de distance entre deux villes de ", results[0].max_city_distance)
    print("l'écart moyen entre la durée du parcours et le manque de temps de livraison est de ", écartDureeParcoursMissmatch, " avec un maximum de temps de livraison de ", results[0].max_delivery_win_len)
    print()