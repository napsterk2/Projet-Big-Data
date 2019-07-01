import time
import os
import psutil
from multiprocessing import Process

from mongoengine import connect

from program.algo.algo_neighborhood import tabu_search
from program.instance_generation import *
from program.report import ExecutionReport


def analyze_ram_usage(target_list: [], is_running: [bool]) -> None:
    """
    Writes to an array the RAM usage as bytes every 0.1 sec

    :param target_list: The list where to write the ram usage
    :param is_running: Boolean passed as an array to pass it by reference instead of value
    :return:
    """
    while is_running[0]:
        target_list.append(psutil.Process(os.getpid()).memory_info().rss)


def run_algo(algo, max_city_dist, max_delivery_win_len, **kwargs) -> ExecutionReport:
    start_time = time.time()
    # ram_analyzer.start()
    result = algo(**kwargs)
    end_time = time.time()
    report = ExecutionReport(exec_time=end_time - start_time,
                             algo_result=result,
                             max_city_distance=max_city_dist,
                             max_window_delivery_len=max_delivery_win_len)
    report.save()
    return report


def run_multistart(algo, nb_processes: int, max_city_dist: int, max_delivery_win_len: int, **kwargs):
    results = []
    for i in range(nb_processes):
        Process(target=run_algo, args=(algo, max_city_dist, max_delivery_win_len, kwargs)).start()


if __name__ == '__main__':
    connect('projet-big-data', host='34.76.156.13', port=8181)
    windows = generate_objects_delivery_window(1000, 3000)
    first_solution = generate_close2realistic_solution(windows)
    # first_solution = generate_random_solution(1000)
    result = run_algo(tabu_search,
                      3000, 3000,
                      starting_solution=first_solution,
                      tabu_list_size=20,
                      max_iter_nb=20,
                      objects_delivery_window=windows,
                      road_net_adjacency_matrix=generate_road_network_adjacency_matrix(1000, 3000)
                      )
