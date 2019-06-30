import random


class NotEnoughCitiesException(Exception):

    def __init__(self, message):

        super().__init__(message)


def generate_road_network_adjacency_matrix(nbr_cities: int, max_distance: int) -> [[int]]:
    """
    Generates an Adjacency Matrix modeling an instance of the problem.

    :param nbr_cities: number of cities for the problem instance
    :param max_distance: the max distance between two different cities
    :return: an Adjacency Matrix
    """

    if nbr_cities < 1000:
        raise NotEnoughCitiesException("The number of cities has to be at least 1000")

    # Initialize the matrix
    city_base_array = [-1] * nbr_cities
    matrix = [city_base_array] * nbr_cities

    # Randomly generates the distance between each city.
    for i in range(nbr_cities):

        for j in range(nbr_cities):

            # Distance between a same city has to be 0
            if i == j:
                matrix[i][j] = 0
            elif matrix[i][j] == -1:
                curr_dist = random.randint(1, max_distance)
                matrix[i][j] = curr_dist
                matrix[j][i] = curr_dist

    return matrix


def generate_objects_delivery_window(nbr_objects: int, max_delivery_deadline: int) -> [(int, int)]:
    """
    Generates the delivery window for each object where object number i has to be delivered to city number i

    :param nbr_objects: The number of objects to deliver, should be equal to the number of cities for a problem instance
    :param max_delivery_deadline: The maximum delay for any object to be delivered
    :return: A list of tuple where the first element of the tuple is the start of the delivery window and the second
    element is the end of the delivery window for the object i where i is the current list index
    """

    result_array = []
    for i in range(nbr_objects):
        # Keeping the randomly generated delivery window start is here needed to make sure that the number modeling the
        # end of the window is greater than the one modeling the start
        delivery_window_start = random.randint(0, max_delivery_deadline)
        result_array.append((delivery_window_start, random.randint(delivery_window_start, max_delivery_deadline)))

    return result_array


def generate_random_solution(nbr_cities: int) -> [int]:
    """
    Generates a random solution that may be realistic or not

    :param nbr_cities: the number of cities for the problem instance
    :return: a list of the cities reached by order
    """
    cities_list = list(range(nbr_cities))
    solution = []
    while len(cities_list) > 0:
        _ = random.choice(cities_list)
        solution.append(_)
        cities_list.remove(_)

    return solution
