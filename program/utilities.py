def generate_solution_neighbors(curr_solution: [int]) -> [[int]]:
    """
    Generates a list of neighbors for a solution where a neighbor is the solution + 1 computation between element x
    and x +1.

    :param curr_solution: A list of int representing the order the cities are visited
    :return: A list of neighbors (list of int also representing the order the cities are reached)
    """
    neighbors = []
    for i in range(len(curr_solution) - 1):
        # We need to copy the solution since list are mutable
        temp_solution = curr_solution.copy()
        # Compute two elements of the list
        _ = temp_solution[i]
        temp_solution[i] = temp_solution[i + 1]
        temp_solution[i + 1] = _
        neighbors.append(temp_solution)

    return neighbors


def evaluate_solution_path_len(solution: [int], road_net_adjacency_matrix: [[int]]) -> int:
    """
    Evaluates the length of the path for the input solution

    :param solution: A list of number representing visited cities
    :param road_net_adjacency_matrix: the adjacency matrix of the graph containing the distances between cities
    :return: The length of the path as an int
    """
    distance = 0
    for index, city in enumerate(solution):

        # If we the current city is the last one, add the length between it and the first city of the list
        if index == len(solution) - 1:
            distance += road_net_adjacency_matrix[city][solution[0]]
        else:
            distance += road_net_adjacency_matrix[city][solution[index + 1]]

    return distance


def evaluate_solution_path_duration(solution: [int], road_net_adjacency_matrix: [[int]],
                                    obj_delivery_windows: [(int, int)]) -> int:
    """
    Evaluates the duration of the path journey for the input solution

    :param solution: A list of number representing visited cities
    :param road_net_adjacency_matrix: the adjacency matrix of the graph containing the distances between cities
    :param obj_delivery_windows: A list of tuple where a tuple at index x represents the object to be delivered at
    city x. The first element of the tuple is the opening of the delivery window and the last one is the end of it
    :return: The duration of the path journey as an int
    """

    # Duration is initialized with the amount of time we need to wait to deliver the first object
    duration = obj_delivery_windows[solution[0]][0]
    for index, city in enumerate(solution[1:]):

        # If the spent duration is less than the opening of the delivery window for the next object to deliver, wait for
        # it opening
        if duration < obj_delivery_windows[city][0]:
            duration += obj_delivery_windows[city][0] - duration
        duration += road_net_adjacency_matrix[city][solution[index - 1]]

    # Add the duration for the final journey to get back to the starting city
    duration += road_net_adjacency_matrix[solution[len(solution) - 1]][solution[0]]
    return duration


def evaluate_solution_delivery_window_missmatch(solution: [int], road_net_adjacency_matrix: [[int]],
                                                obj_delivery_windows: [(int, int)]) -> int:
    """
    Evaluates the global difference between expected delivery time and real delivery time for each object

    :param solution: A list of number representing visited cities
    :param road_net_adjacency_matrix: the adjacency matrix of the graph containing the distances between cities
    :param obj_delivery_windows: A list of tuple where a tuple at index x represents the object to be delivered at
    city x. The first element of the tuple is the opening of the delivery window and the last one is the end of it
    :return: The total missmatch of the deliveries as an int
    """
    total_missmatch = 0

    for index, city in enumerate(solution[1:]):
        city_arrive_time = evaluate_solution_path_duration(solution[:index + 1], road_net_adjacency_matrix,
                                                           obj_delivery_windows)
        if city_arrive_time > obj_delivery_windows[city][1]:
            total_missmatch += city_arrive_time - obj_delivery_windows[city][1]

    return total_missmatch


def evaluate_solution(solution: [int], road_net_adjacency_matrix: [[int]], obj_delivery_windows: [(int, int)]) -> int:
    """
    Evaluates the global quality of the solution with a scalar approach

    :param solution: A list of number representing visited cities
    :param road_net_adjacency_matrix: the adjacency matrix of the graph containing the distances between cities
    :param obj_delivery_windows: A list of tuple where a tuple at index x represents the object to be delivered at
    city x. The first element of the tuple is the opening of the delivery window and the last one is the end of it
    :return: An int representing the global quality of the solution
    """
    return 2 * evaluate_solution_path_len(solution, road_net_adjacency_matrix) \
            + evaluate_solution_delivery_window_missmatch(solution, road_net_adjacency_matrix, obj_delivery_windows) \
            + evaluate_solution_path_duration(solution, road_net_adjacency_matrix, obj_delivery_windows)
