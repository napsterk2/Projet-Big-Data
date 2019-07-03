from livrable.livrable_tec.algorithm.tabu_search import tabu_search
from livrable.livrable_tec.dataset.random_generation import generate_road_network_adjacency_matrix, \
    generate_objects_delivery_window, generate_random_solution


def load_test_by_cities_nb(max_nb_cities: int):
    max_city_distance = 6000
    max_del_win_len = 12000
    print("============= Load Test by Cities nb ============================")
    for i in range(max_nb_cities):
        matrix = generate_road_network_adjacency_matrix(i, max_city_distance)
        windows = generate_objects_delivery_window(i, max_del_win_len)
        result = tabu_search(
            max_city_distance=max_city_distance,
            max_del_win_len=max_del_win_len,
            starting_solution=generate_random_solution(i),
            max_iter_nb=60,
            tabu_list_size=20,
            objects_delivery_window=windows,
            road_net_adjacency_matrix=matrix
        )
        print("Nb Cities : " + str(i) + " | Nb Iter : 60 | Execution time : " + str(result.exec_time))


def load_test_by_iter_nb(max_iter_nb: int):
    max_city_distance = 6000
    max_del_win_len = 12000
    print("============= Load Test by iter nb ============================")
    for i in range(max_iter_nb):
        matrix = generate_road_network_adjacency_matrix(100, max_city_distance)
        windows = generate_objects_delivery_window(100, max_del_win_len)
        result = tabu_search(
            max_city_distance=max_city_distance,
            max_del_win_len=max_del_win_len,
            starting_solution=generate_random_solution(100),
            max_iter_nb=i,
            tabu_list_size=20,
            objects_delivery_window=windows,
            road_net_adjacency_matrix=matrix
        )
        print("Nb Cities : 100 | Nb Iter : " + str(i) + " | Execution time : " + str(result.exec_time))
