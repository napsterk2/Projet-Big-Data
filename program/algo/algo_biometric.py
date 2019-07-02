import random
import time

from program.instance_generation import generate_road_network_adjacency_matrix, generate_random_solution

"Fonction de selection d'une arrète lors du déplacement d'une fourmie"
def edge_selection(id_city: int) -> int:

    for i in range(nbr_cities):

        selected_city = random.randint(0, nbr_cities-1)

        if visited_cities.count(selected_city) == 0:
            return selected_city


"Fonction de mise à jour des niveaux de pheromone: depôt et évaporation"
def trail_update(id_ant: int):
    pass


"Nombre de villes"
nbr_cities = 10
distance_max = 100
"Population de fourmie"
ants = 10

ants_path = []
path_base_array = [0] * nbr_cities
for i in range(ants):
    ants_path.append(path_base_array.copy())

"Matrice gardant les niveaux de pheromones"
trails_matrix = []
base_array = [0.00] * nbr_cities
for i in range(nbr_cities):
    trails_matrix.append(base_array.copy())

"on genère les villes et les distances entres les villes"
distance_matrix = generate_road_network_adjacency_matrix(nbr_cities, distance_max)

"On genère une première solution aléatoire en tant que fourmie éclaireuse"
scout_path = generate_random_solution(nbr_cities)

"Calcul de la distance parcourue par l'eclaireuse"
total_distance_scout = 0
for i in range(len(scout_path)):
    if i < nbr_cities -1:
        x = scout_path[i]
        y = scout_path[i+1]
    else:
        x = scout_path[i]
        y = scout_path[0]

    total_distance_scout += distance_matrix[x][y]

"Dépot de pheromones sur les arrètes parcourues par la fourmie éclaireuse"
for i in range(len(scout_path)):
    if i < nbr_cities - 1:
        x = scout_path[i]
        y = scout_path[i + 1]
    else:
        x = scout_path[i]
        y = scout_path[0]

    trails_matrix[x][y] = round(100.0/total_distance_scout, 2)
    trails_matrix[y][x] = round(100.0/total_distance_scout, 2)

print('chemin initial ', scout_path)
print('distance parcourue: ', total_distance_scout)
for i in range(len(trails_matrix)):
    print(trails_matrix[i])

"On récupère la ville de départ"
start_city = scout_path[0]

termination = False

"""for i in range(ants):
    print(ants_path[i])"""

while not termination:

    for i in range(ants):

        print('\nfourmi: ', i)
        visited_cities = []
        current_city = start_city
        index = 0

        for j in range(nbr_cities):
            ants_path[i].append(current_city)
            visited_cities.append(current_city)

            next_city = edge_selection(current_city)

            current_city = next_city
            index += 1

        print(ants_path[i])


