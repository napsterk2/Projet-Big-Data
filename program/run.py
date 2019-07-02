import os
import psutil
from multiprocessing import Process

from mongoengine import connect

from program.algo.algo_neighborhood import tabu_search
from program.instance_generation import *


def analyze_ram_usage(target_list: [], is_running: [bool]) -> None:
    """
    Writes to an array the RAM usage as bytes every 0.1 sec

    :param target_list: The list where to write the ram usage
    :param is_running: Boolean passed as an array to pass it by reference instead of value
    :return:
    """
    while is_running[0]:
        target_list.append(psutil.Process(os.getpid()).memory_info().rss)


def run_tabu_search_multistart(nb_runs, adjacency_matrix, obj_del_window):
    for i in range(nb_runs):
        tabu_search(generate_random_solution(len(obj_del_window)), 20, 40, windows, matrix)


if __name__ == '__main__':
    connect('projet-big-data', host='34.76.156.13', port=8181)
    nb_cities = 1000
    matrix = generate_road_network_adjacency_matrix(nb_cities, 6000)
    windows = generate_objects_delivery_window(nb_cities, 12000)
    run_tabu_search_multistart(6, matrix, windows)
