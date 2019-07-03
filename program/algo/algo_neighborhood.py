import time

from program.report import AlgoResult
from program.utilities import generate_solution_neighbors, evaluate_solution


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
    start_time = time.time()

    while iter_nb < max_iter_nb:
        # print("Iteration : " + str(iter_nb))
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

        local_optimum_value_history.append(local_optimum_value)

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
    return AlgoResult(
        adjacency_matrix= road_net_adjacency_matrix,
        iter_nb=iter_nb,
        max_city_distance=max_city_distance,
        global_optimum=global_optimum,
        local_optimum_value_history=local_optimum_value_history,
        exec_time=end_time - start_time,
        starting_solution=starting_solution,
        objects_delivery_window=objects_delivery_window,
        max_delivery_win_len=max_del_win_len
    )
