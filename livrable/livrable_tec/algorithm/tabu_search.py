import time
from threading import Thread

from .result_class import AlgoResult
from .utilities import evaluate_solution_path_len, evaluate_solution_path_duration, \
    evaluate_solution_delivery_window_missmatch, evaluate_solution, analyze_ram_usage, generate_solution_neighbors
from ..dataset.random_generation import generate_random_solution


def tabu_search(starting_solution: [int], tabu_list_size: int, max_iter_nb: int, objects_delivery_window: [(int, int)],
                road_net_adjacency_matrix: [[int]], max_city_distance: int, max_del_win_len: int) -> AlgoResult:
    """
    Iterates over solutions neighbor with a list of forbidden solutions to find the global optimum

    :param max_del_win_len: Maximum temporal delivery windows length
    :param max_city_distance: Maximum possible distance between two cities
    :param starting_solution: The list of visited cities as a list of int
    :param tabu_list_size: Max size of the tabu list
    :param max_iter_nb: Max number of iterations
    :param objects_delivery_window: List of tuple where the element at position x represents the delivery windows for
    the object x. The first element of the tuple is the opening of the delivery windows and the second element is the
    end of it
    :param road_net_adjacency_matrix: Adjacency matrix representing the distance between cities
    :return: AlgoResult object holding information about the function execution
    """
    iter_nb = 0
    current_solution = starting_solution.copy()
    tabu_list = []

    global_optimum = starting_solution
    global_optimum_value = evaluate_solution(starting_solution, road_net_adjacency_matrix, objects_delivery_window)

    # Stats variables
    local_optimum_value_history = []
    ram_usage = []
    analyze_ram = [True]
    ram_analyzer = Thread(target=analyze_ram_usage, args=(ram_usage, analyze_ram))
    ram_analyzer.start()
    start_time = time.time()

    while iter_nb < max_iter_nb:
        local_optimum_value = None
        local_optimum = []
        # For each neighbor, check if it is a realistic solution and if its value is better than the old one for this
        # neighbor's solution iteration
        for neighbor in generate_solution_neighbors(current_solution):

            if neighbor not in tabu_list:
                neighbor_value = evaluate_solution(neighbor, road_net_adjacency_matrix, objects_delivery_window)
                if local_optimum_value is None or neighbor_value < local_optimum_value:
                    local_optimum_value = neighbor_value
                    local_optimum = neighbor

        local_optimum_value_history.append({
            'del_missmatch': evaluate_solution_delivery_window_missmatch(local_optimum, road_net_adjacency_matrix,
                                                                         objects_delivery_window),
            'journey_duration': evaluate_solution_path_duration(local_optimum, road_net_adjacency_matrix,
                                                                objects_delivery_window),
            'path_len': evaluate_solution_path_len(local_optimum, road_net_adjacency_matrix)
        })

        # Add the best neighbor found to the tabu_list
        tabu_list.append(local_optimum)
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)

        # Update global optimum if needed
        if local_optimum_value < global_optimum_value:
            global_optimum_value = local_optimum_value
            global_optimum = local_optimum

        current_solution = local_optimum
        iter_nb += 1

    end_time = time.time()
    analyze_ram[0] = False
    ram_analyzer.join()
    return AlgoResult(
        adjacency_matrix=road_net_adjacency_matrix,
        iter_nb=iter_nb,
        max_city_distance=max_city_distance,
        global_optimum=global_optimum,
        local_optimum_value_history=local_optimum_value_history,
        exec_time=end_time - start_time,
        starting_solution=starting_solution,
        objects_delivery_window=objects_delivery_window,
        max_delivery_win_len=max_del_win_len,
        avg_ram=(sum(ram_usage) / len(ram_usage)) / 1000000,
        tabu_list_size=tabu_list_size
    )


def tabu_search_multistart(nb_runs, nb_iter, tabu_list_size, adjacency_matrix, obj_del_window, max_city_distance,
                           max_del_win_len) -> [AlgoResult]:
    """
    Runs a tabu search using the multistart method

    :param nb_runs:
    :param nb_iter:
    :param tabu_list_size:
    :param adjacency_matrix:
    :param obj_del_window:
    :param max_city_distance:
    :param max_del_win_len:
    :return:
    """
    results = []
    for i in range(nb_runs):
        results.append(
            tabu_search(generate_random_solution(len(obj_del_window)), tabu_list_size, nb_iter, obj_del_window,
                        adjacency_matrix, max_city_distance, max_del_win_len)
        )
    return results