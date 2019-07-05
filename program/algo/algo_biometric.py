import random
import time

from program.instance_generation import generate_road_network_adjacency_matrix, generate_random_solution

"Fonction de selection d'une arrète lors du déplacement d'une fourmie"
def edge_selection(id_city: int, id_ant: int, remaining_cities: [int]) -> int:

    visibility = [0] * nbr_cities
    trail = [0] * nbr_cities
    atractiveness = [0] * nbr_cities
    total_atract = 0.0
    move_proba = [0] * nbr_cities
    frequency_tab = []

    for i in remaining_cities:
        visibility[i] = round(1/distance_matrix[id_city][i], 5)
        trail[i] = trails_matrix[id_city][i]
        atractiveness[i] = gamma + round(((visibility[i]) * alpha) * (trail[i] * beta), 5)
        total_atract = total_atract + atractiveness[i]

    for j in remaining_cities:
        move_proba[j] = round(atractiveness[j] / total_atract, 5)

        if int(move_proba[j]*100) != 0:
            for k in range(int(move_proba[j] * 100)):
                frequency_tab.append(j)
        else:
            frequency_tab.append(j)

    print(move_proba)

    selected_city = random.choice(frequency_tab)
    return selected_city

"Fonction de mise à jour des niveaux de pheromone: depôt et évaporation"
def trail_deposit(id_ant: int):
    total_distance = 0
    for i in range(len(ants_path[id_ant])):
        if i < nbr_cities - 1:
            x = ants_path[id_ant][i]
            y = ants_path[id_ant][i+1]
        else:
            x = ants_path[id_ant][i]
            y = ants_path[id_ant][0]

        total_distance += distance_matrix[x][y]

    for i in range(len(ants_path[id_ant])):
        if i < nbr_cities - 1:
            x = ants_path[id_ant][i]
            y = ants_path[id_ant][i+1]
        else:
            x = ants_path[id_ant][i]
            y = ants_path[id_ant][0]

        temporary_trail_matrix[x][y] = round(temporary_trail_matrix[x][y] + (quotient_div / total_distance), 5) * 2

    print('distance parcourue: ', total_distance)
    print('depot de pheromones: ', round((quotient_div / total_distance), 5))

def trail_evaporation():
    for i in range(len(trails_matrix)):
        for j in range(len(trails_matrix[i])):
            trails_matrix[i][j] = round((1 - 0.5) * trails_matrix[i][j], 5)

"Nombre de villes"
nbr_cities = 25
distance_max = 100
"Population de fourmie"
ants = 15

"Quotient pour les différents calculs"
alpha = 2.0
beta = 4.0
gamma = 0.1

quotient_div = nbr_cities * distance_max

"Matrice gardant les niveaux de pheromones"
trails_matrix = []
base_array = [0.00] * nbr_cities
for n in range(nbr_cities):
    trails_matrix.append(base_array.copy())

"on genère les villes et les distances entres les villes"
distance_matrix = generate_road_network_adjacency_matrix(nbr_cities, distance_max)
for d in range(len(distance_matrix)):
    print(distance_matrix[d])

"On genère une première solution aléatoire en tant que fourmie éclaireuse"
scout_path = generate_random_solution(nbr_cities)

"Calcul de la distance parcourue par l'eclaireuse"
total_distance_scout = 0
for s in range(len(scout_path)):
    if s < nbr_cities -1:
        x = scout_path[s]
        y = scout_path[s+1]
    else:
        x = scout_path[s]
        y = scout_path[0]

    total_distance_scout += distance_matrix[x][y]

"Dépot de pheromones sur les arrètes parcourues par la fourmie éclaireuse"
for s in range(len(scout_path)):
    if s < nbr_cities - 1:
        x = scout_path[s]
        y = scout_path[s + 1]
    else:
        x = scout_path[s]
        y = scout_path[0]
    "Calcul de la quantité de pheromones a deposer"
    trails_matrix[x][y] = round(quotient_div/total_distance_scout, 5)
    "trails_matrix[y][x] = round(quotient_div/total_distance_scout, 5)"

print('chemin initial ', scout_path)
print('distance parcourue: ', total_distance_scout)
for t in range(len(trails_matrix)):
    print(trails_matrix[t])

"On récupère la ville de départ"
start_city = scout_path[0]

termination = False

"""for i in range(ants):
    print(ants_path[i])"""
iteration_counter = 0
while not termination:
    print('\niteration: ', iteration_counter)

    ants_path = []
    path_base_array = [0] * nbr_cities
    for a in range(ants):
        ants_path.append(path_base_array.copy())

    temporary_trail_matrix = []
    matrix_base_array = [0] * nbr_cities
    for i in range(nbr_cities):
        temporary_trail_matrix.append(matrix_base_array.copy())

    for a in range(ants):
        print('\nfourmi: ', a)
        remaining_cities = []
        "Liste des villes restantes a parcourir pour la fourmi i"
        for n in range(nbr_cities):
            remaining_cities.append(n)

        current_city = start_city

        for c in range(nbr_cities):
            ants_path[a][c] = current_city
            remaining_cities.remove(current_city)
            if len(remaining_cities) != 0:
                next_city = edge_selection(current_city, a, remaining_cities)
                current_city = next_city

        trail_deposit(a)
        print(ants_path[a],'\n')

    "évaporation des anciennes pheromones"
    trail_evaporation()

    "Apres évaporation des phéromones de l'itération précédente, on rajoute les phéromones de l'itération courante"
    for i in range(len(trails_matrix)):
        for j in range(len(trails_matrix)):
            trails_matrix[i][j] = round(trails_matrix[i][j] + temporary_trail_matrix[i][j], 5)

    iteration_counter += 1

    "Critère d'arret : 1000 itérations effectuées"
    if iteration_counter == 300:
        termination = True

