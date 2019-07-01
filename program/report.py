
from mongoengine import DynamicDocument, DynamicEmbeddedDocument


class AlgoMethod:
    TABU_SEARCH = "TABU_SEARCH"


class AlgoResult(DynamicEmbeddedDocument):

    def __init__(self, local_optimum_history: [[int]], local_optimum_value_history: [int], global_optimum_found: [int],
                 global_optimum_value: int, non_realistic_solutions_met_percentage: float, used_algo: AlgoMethod,
                 adjacency_matrix: [[int]], objects_delivery_window: [(int, int)]) -> None:
        super().__init__()
        self.local_opt_hist = local_optimum_history
        self.local_opt_val_hist = local_optimum_value_history
        self.global_opt = global_optimum_found
        self.global_opt_val = global_optimum_value
        self.non_real_sol_percent = non_realistic_solutions_met_percentage
        self.used_algo = used_algo
        self.adjacency_matrix = adjacency_matrix
        self.objects_delivery_window = objects_delivery_window


class ExecutionReport(DynamicDocument):

    def __init__(self, exec_time: float, avg_ram_usage: int, iter_nb: int, algo_result: AlgoResult) -> None:
        super().__init__()
        self.exec_time = exec_time
        self.ram_usage = avg_ram_usage
        self.iter_nb = iter_nb
        self.algo_result = algo_result
