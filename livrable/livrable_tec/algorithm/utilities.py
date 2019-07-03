import os
import time

import psutil


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

        # If the current city is the last one, add the length between it and the first city of the list
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
    for index, city in enumerate(solution):

        if index == len(solution) - 1:
            # Add the duration for the final journey to get back to the starting city
            duration += road_net_adjacency_matrix[solution[len(solution) - 1]][solution[0]]
        else:
            duration += road_net_adjacency_matrix[city][solution[index + 1]]
            # If the truck arrives before the opening of the deliver window, it has to wait for the opening of it
            if duration < obj_delivery_windows[solution[index + 1]][0]:
                duration += obj_delivery_windows[solution[index + 1]][0] - duration

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

    for index, city in enumerate(solution):

        # Prevents index out of bound
        if index != len(solution) - 1:

            city_arrive_time = evaluate_solution_path_duration(solution[:index + 1], road_net_adjacency_matrix,
                                                               obj_delivery_windows)
            # If the actual time is greater than the max delivery time for the current object, increase missmatch with
            # the difference
            if city_arrive_time > obj_delivery_windows[solution[index + 1]][1]:
                total_missmatch += city_arrive_time - obj_delivery_windows[city][1]

    return total_missmatch


def evaluate_solution(solution: [int], road_net_adjacency_matrix: [[int]], obj_delivery_windows: [(int, int)]) -> float:
    """
    Evaluates the global quality of the solution with a scalar approach, weights on objectives functions have been
    chosen arbitrarily

    :param solution: A list of number representing visited cities
    :param road_net_adjacency_matrix: the adjacency matrix of the graph containing the distances between cities
    :param obj_delivery_windows: A list of tuple where a tuple at index x represents the object to be delivered at
    city x. The first element of the tuple is the opening of the delivery window and the last one is the end of it
    :return: An int representing the global quality of the solution
    """
    return evaluate_solution_path_len(solution, road_net_adjacency_matrix) \
            + evaluate_solution_delivery_window_missmatch(solution, road_net_adjacency_matrix, obj_delivery_windows) \
            + 0.5 * evaluate_solution_path_duration(solution, road_net_adjacency_matrix, obj_delivery_windows)


def analyze_ram_usage(target_list: [], is_running: [bool]) -> None:
    """
    Writes to an array the RAM usage as bytes every 0.1 sec

    :param target_list: The list where to write the ram usage
    :param is_running: Boolean passed as an array to pass it by reference instead of by value
    :return:
    """
    while is_running[0]:
        target_list.append(psutil.Process(os.getpid()).memory_info().rss)
        time.sleep(1)
