from mongoengine import DynamicDocument

from .utilities import *


class AlgoResult(DynamicDocument):
    """
    A class holding properties about a algorithm execution
    """

    def __init__(self, starting_solution: [int], iter_nb: int, exec_time: float, global_optimum: [int],
                 adjacency_matrix: [[int]], objects_delivery_window: [(int, int)], tabu_list_size: int, avg_ram: float,
                 local_optimum_value_history: [], max_delivery_win_len: int, max_city_distance: int) -> None:
        super().__init__()
        self.nbr_cities = len(starting_solution)
        self.iter_nb = iter_nb
        self.exec_time = exec_time
        self.global_opt = global_optimum
        self.global_opt_path_len = evaluate_solution_path_len(global_optimum, adjacency_matrix)
        self.global_opt_win_missmatch = \
            evaluate_solution_delivery_window_missmatch(global_optimum, adjacency_matrix, objects_delivery_window)
        self.global_opt_journey_duration = \
            evaluate_solution_path_duration(global_optimum, adjacency_matrix, objects_delivery_window)
        self.adjacency_matrix = adjacency_matrix
        self.objects_delivery_window = objects_delivery_window
        self.local_optimum_value_history = local_optimum_value_history
        self.max_delivery_win_len = max_delivery_win_len
        self.max_city_distance = max_city_distance
        self.tabu_list_size = tabu_list_size
        self.avg_ram_usage = avg_ram
