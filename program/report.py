
from mongoengine import DynamicDocument, DynamicEmbeddedDocument

from program.utilities import is_solution_realistic


class AlgoMethod:
    TABU_SEARCH = "TABU_SEARCH"


class AlgoResult(DynamicEmbeddedDocument):

    def __init__(self, starting_solution: [int], max_iter_nb: int, iter_nb_done: int, global_optimum_found: [int],
                 global_optimum_value: int, non_realistic_solutions_met_percentage: float, used_algo: AlgoMethod,
                 adjacency_matrix: [[int]], objects_delivery_window: [(int, int)], local_optimum_value_history: [int]) \
            -> None:
        super().__init__()
        self.nbr_cities = len(starting_solution)
        self.is_starting_solution_realistic = is_solution_realistic(starting_solution, objects_delivery_window)
        self.max_iter_nb = max_iter_nb
        self.nb_iter_done = iter_nb_done
        self.starting_solution = starting_solution
        self.global_opt = global_optimum_found
        self.global_opt_val = global_optimum_value
        self.non_real_sol_percent = non_realistic_solutions_met_percentage
        self.used_algo = used_algo
        self.adjacency_matrix = adjacency_matrix
        self.objects_delivery_window = objects_delivery_window
        self.local_optimum_value_history = local_optimum_value_history


class ExecutionReport(DynamicDocument):

    def __init__(self, exec_time: float, algo_result: AlgoResult, max_city_distance: int, max_window_delivery_len: int) -> None:
        super().__init__()
        self.exec_time = exec_time
        self.max_city_distance = max_city_distance
        self.max_window_delivery_len = max_window_delivery_len
        self.algo_result = algo_result
