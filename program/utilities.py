def generate_solution_neighbors(curr_solution: [int]) -> [[int]]:
    """
    Generates a list of neighbors for a solution where a neighbor is the solution + 1 computation.

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


def evaluate_solution(solution: [int], road_net_adjacency_matrix: [[int]]) -> int:
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


def is_solution_realistic(solution: [int], objects_delivery_window: [(int, int)]) -> bool:
    """
    Checks whether a solution is a realistic one or not considering the fact that it is possible to wait for a delivery
    window opening

    :param solution: A list of number representing visited cities
    :param objects_delivery_window: A list of tuple where a tuple at index x represents the object to be delivered at
    city x. The first element of the tuple is the opening of the delivery window and the last one is the end of it
    :return: True if the solution is realistic, else no
    """
    time = 0
    for city in solution:

        if time > objects_delivery_window[city][1]:
            return False
        elif time < objects_delivery_window[city][0]:
            time = objects_delivery_window[city][0]
    return True
