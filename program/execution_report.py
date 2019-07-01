from enum import Enum


class AlgoMethods(Enum):
    TABU_SEARCH = 1


class ExecutionReport:

    def __init__(self, exec_time: int, ram_usage, cities_nb, iter_nb, adjacency_matrix, delivery_windows,
                 non_realistic_solutions_met_percentage, local_optimum_history, global_optimum_found, used_method) -> None:
        super().__init__()
