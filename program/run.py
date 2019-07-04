from mongoengine import connect

from program.algo.algo_neighborhood import tabu_search
from program.instance_generation import *
from program.report import AlgoResult
from program.Statistic import *

from program.CalculGraph import *


def run_tabu_search_multistart(nb_runs, nb_iter, tabu_list_size, adjacency_matrix, obj_del_window, max_city_distance,
                               max_del_win_len) -> [AlgoResult]:
    results = []
    for i in range(nb_runs):
        results.append(
            tabu_search(generate_random_solution(len(obj_del_window)), tabu_list_size, nb_iter, obj_del_window,
                        adjacency_matrix, max_city_distance, max_del_win_len)
        )

    print ("======================== STATS ===================")
    temps_exec_cities(results)
    ram_cities(results)
    moyenne_distances(results)
    temps_exec_itteration(results)
    ecart_optimum_local(results)
    écart_temps_parours_missmatch_ecart_max_villes_obj_plus_tard(results)

    return results


if __name__ == '__main__':
    connect('projet-big-data', host='34.76.156.13', port=8181)
    nb_cities = 200
    max_city_distance = 6000
    max_del_win_len = 12000
    matrix = generate_road_network_adjacency_matrix(nb_cities, max_city_distance)
    cl = GraphCalculation(matrix)
    windows = generate_objects_delivery_window(nb_cities, max_del_win_len)

    for index, result in enumerate(run_tabu_search_multistart(5, 100, 40, matrix, windows, max_city_distance, max_del_win_len)):
        result.save()
        print("=============== RUN  " + str(index + 1) + "===============")
        print("Global optimum path length : " + str(result.global_opt_path_len))
        print("Global optimum delivery windows missmatch : " + str(result.global_opt_win_missmatch))
        print("Global optimum journey duration : " + str(result.global_opt_journey_duration))
        print()
