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
    global_optimum_value = evaluate_solution(starting_solution, road_net_adjacency_matrix)
    global_optimum = starting_solution

    while iter_nb < max_iter_nb:

        local_optimum_value = 0
        local_optimum = []
        # For each neighbor, check if it is a realistic solution and if its value is better than the old one for this
        # neighbor's solution iteration
        for neighbor in generate_solution_neighbors(current_solution):

            if neighbor not in tabu_list and is_solution_realistic(neighbor, objects_delivery_window):
                neighbor_value = evaluate_solution(neighbor, road_net_adjacency_matrix)
                if neighbor_value > local_optimum_value:
                    local_optimum_value = neighbor_value
                    local_optimum = neighbor

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

    return global_optimum, global_optimum_value
