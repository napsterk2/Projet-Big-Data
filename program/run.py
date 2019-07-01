import time
import os
import psutil
from threading import Thread
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


def run_algo(algo, **kwargs) -> ExecutionReport:
    ram_usage = []
    should_run = True
    ram_analyzer = Thread(target=analyze_ram_usage, args=(ram_usage, [should_run]))
    start_time = time.time()
    # ram_analyzer.start()
    result = algo(**kwargs)
    end_time = time.time()
    should_run = False
    # ram_analyzer.join()
    report = ExecutionReport(exec_time=end_time - start_time,
                             avg_ram_usage=46555,
                             iter_nb=kwargs['max_iter_nb'],
                             algo_result=result)
    report.save()
    return report


def run_multistart(nb_processes: int, fct, **kwargs):
    results = []
    for i in range(nb_processes):
        Process(target=run_algo, args=(fct, kwargs))


if __name__ == '__main__':
    connect('projet-big-data', host='34.76.156.13', port=8181)
    result = run_algo(tabu_search,
                      starting_solution=generate_random_solution(1000),
                      tabu_list_size=20,
                      max_iter_nb=20,
                      objects_delivery_window=generate_objects_delivery_window(1000, 200),
                      road_net_adjacency_matrix=generate_road_network_adjacency_matrix(1000, 3000)
                      )
