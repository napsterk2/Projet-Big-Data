from program.utilities import generate_solution_neighbors, is_solution_realistic, evaluate_solution


def tabu_search(starting_solution: [int], tabu_list_size: int, max_iter_nb: int, objects_delivery_window: [(int, int)],
                road_net_adjacency_matrix: [[int]]):
    iter_nb = 0
    current_solution = starting_solution.copy()
    tabu_list = []
    global_optimum_value = evaluate_solution(starting_solution, road_net_adjacency_matrix)
    global_optimum = starting_solution

    while iter_nb < max_iter_nb:

        local_optimum_value = 0
        local_optimum = []
        for neighbor in generate_solution_neighbors(current_solution):

            if neighbor not in tabu_list and is_solution_realistic(neighbor, objects_delivery_window):
                neighbor_value = evaluate_solution(neighbor, road_net_adjacency_matrix)
                if neighbor_value > local_optimum_value:
                    local_optimum_value = neighbor_value
                    local_optimum = neighbor

        tabu_list.append(local_optimum)
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)

        if local_optimum_value > global_optimum_value:
            global_optimum_value = local_optimum_value
            global_optimum = local_optimum

        current_solution = local_optimum
        iter_nb += 1

    return global_optimum, global_optimum_value
