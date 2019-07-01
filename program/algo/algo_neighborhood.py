from program.report import AlgoResult, AlgoMethod
from program.utilities import generate_solution_neighbors, is_solution_realistic, evaluate_solution


def tabu_search(starting_solution: [int], tabu_list_size: int, max_iter_nb: int, objects_delivery_window: [(int, int)],
                road_net_adjacency_matrix: [[int]]):
    """
    Iterates over solutions neighbor with a list of forbidden solutions to find the global optimum

    :param starting_solution: The list of visited cities as a list of int
    :param tabu_list_size: Max size of the tabu list
    :param max_iter_nb: Max number of iterations
    :param objects_delivery_window: List of tuple where the element at position x represents the delivery windows for
    the object x. The first element of the tuple is the opening of the delivery windows and the second element is the
    end of it
    :param road_net_adjacency_matrix: Adjacency matrix representing the distance between cities
    :return: Tuple where the first element is what is supposed to be the global optimum value, and the second element is
    the solution for the global optimum
    """
    iter_nb = 0
    current_solution = starting_solution.copy()
    tabu_list = []

    if is_solution_realistic(starting_solution, objects_delivery_window):
        global_optimum = starting_solution
        global_optimum_value = evaluate_solution(starting_solution, road_net_adjacency_matrix)
    else:
        global_optimum = []
        global_optimum_value = 0

    # Stats variables
    nb_solutions_analyzed = 0
    nb_non_realistic_solutions_analyzed = 0
    local_optimum_value_history = []

    while iter_nb < max_iter_nb:

        local_optimum_value = 0
        local_optimum = []
        # For each neighbor, check if it is a realistic solution and if its value is better than the old one for this
        # neighbor's solution iteration
        for neighbor in generate_solution_neighbors(current_solution):

            # For stats
            nb_solutions_analyzed += 1
            if is_solution_realistic(neighbor, objects_delivery_window):
                if neighbor not in tabu_list:
                    neighbor_value = evaluate_solution(neighbor, road_net_adjacency_matrix)
                    if neighbor_value > local_optimum_value:
                        local_optimum_value = neighbor_value
                        local_optimum = neighbor
            else:
                nb_non_realistic_solutions_analyzed += 1

        if len(local_optimum) == 0:
            break
        local_optimum_value_history.append(local_optimum_value)

        # Add the best neighbor found to the tabu_list
        tabu_list.append(local_optimum)
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)

        # Update global optimum if needed
        if local_optimum_value > global_optimum_value:
            global_optimum_value = local_optimum_value
            global_optimum = local_optimum

        current_solution = local_optimum
        iter_nb += 1

    result = AlgoResult(
        used_algo=AlgoMethod.TABU_SEARCH,
        adjacency_matrix=road_net_adjacency_matrix,
        objects_delivery_window=objects_delivery_window,
        global_optimum_found=global_optimum,
        global_optimum_value=global_optimum_value,
        starting_solution=starting_solution,
        non_realistic_solutions_met_percentage=nb_non_realistic_solutions_analyzed / nb_solutions_analyzed,
        iter_nb_done=iter_nb,
        max_iter_nb=max_iter_nb,
        local_optimum_value_history=local_optimum_value_history
    )
    result.tabu_list_size = tabu_list_size
    return result
