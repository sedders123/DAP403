import random
import json
import os
import math
import time
import matplotlib.pyplot as plt

from prettytable import PrettyTable
from matplotlib.patches import Rectangle
from collections import OrderedDict

SIMULATION_RUN_COUNT = 5000

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, 'src')
DATA_DIR = os.path.join(SOURCE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')


def load_json_file(file_path):
    '''
    Returns data from a specified JSON file
    '''
    with open(file_path) as data_file:
        tasks = json.load(data_file)
    return tasks


def get_totals(tasks):
    '''
    Returns the sum of all the tasks minimum and maximum times
    '''
    maximum = 0
    minimum = 0
    estimate = 0
    for task in tasks:
        minimum += task["minimum"]
        maximum += task["maximum"]
        estimate += task["estimate"]
    return minimum, maximum, estimate


def run_simulation(minimum, maximum):
    '''
    Runs the simulation and returns the result
    '''
    sim_result = {}
    for i in range(SIMULATION_RUN_COUNT):
        value = random.randint(minimum, maximum)
        for key in range(value, maximum + 1):
            if key not in sim_result:
                sim_result[key] = {"number": 0}
            sim_result[key]["number"] += 1

    for result in sim_result.values():
        result["percentage"] = int((result["number"] / SIMULATION_RUN_COUNT) * 100)

    ordered_sim_result = OrderedDict(sorted(sim_result.items()))
    return ordered_sim_result


def save_graph(result, estimate):
    '''
    Plots and then saves graph of results
    '''
    plt.figure(1)
    plt.style.use('classic')
    fig, ax = plt.subplots()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    # Set up legend
    estimateKey = Rectangle((0, 0), 0.5, 0.5, color='y')
    ax.legend([estimateKey], ["Estimate"])

    x_values = list(result.keys())
    y_values = [sim_result["percentage"] for sim_result in result.values()]
    bars = ax.barh(x_values, y_values, color='r')
    for bar in bars:
        if math.floor(bar.get_y()) == estimate:
            bar.set_color('y')
    for i, value in enumerate(y_values):
        ax.text(value + 3, x_values[i] + 0.5, "{}%".format(str(value)), color='blue', fontweight='bold')

    # Hide major tick labels
    ax.set_yticklabels('')

    # Customize minor tick labels to place in center
    ax.set_yticks([sim_result + 0.5 for sim_result in result], minor=True)
    ax.set_yticklabels([sim_result for sim_result in result], minor=True)

    plt.gca().invert_yaxis()
    plt.title('Monte Carlo Simulation')
    plt.xlabel('Percentage')
    plt.ylabel('Time')

    plt.savefig(os.path.join(OUTPUT_DIR, 'chart.png'))
    plt.close()


def create_table(result, estimate):
    '''
    Generates a pretty printed table output of the results
    '''
    table = PrettyTable()
    is_estimate = []
    for sim_result in result:
        is_estimate.append("X") if sim_result == estimate else is_estimate.append("")
    table.add_column("Time", list(result.keys()))
    table.add_column("Number of times (Out of {})".format(SIMULATION_RUN_COUNT), [sim_result["number"] for sim_result in result.values()])
    table.add_column("Percent of total (rounded)", [sim_result["percentage"] for sim_result in result.values()])
    table.add_column("Estimate", is_estimate)
    return table


def test_performance():
    global SIMULATION_RUN_COUNT
    ones = [int('1' + '0' * i) for i in range(5)]
    fives = [int('5' + '0' * i) for i in range(5)]
    runs_to_try = sorted(ones + fives)
    total_times = []

    tasks_file = os.path.join(DATA_DIR, 'tasks.json')
    tasks = load_json_file(tasks_file)
    minimum, maximum, estimate = get_totals(tasks)

    for i in runs_to_try:
        SIMULATION_RUN_COUNT = i
        start_simulation = time.time()
        run_simulation(minimum, maximum)
        end_simulation = time.time()
        total_time = end_simulation - start_simulation
        total_times.append(total_time)

    # Create Graph
    plt.figure(2)
    plt.ylabel("Time(s)")
    plt.xlabel("Number of runs")
    plt.title("Performance of Monte Carlo implementation")
    plt.plot(runs_to_try, total_times)
    plt.savefig(os.path.join(OUTPUT_DIR, 'performance.png'))
    plt.close()


if __name__ == '__main__':
    tasks_file = os.path.join(DATA_DIR, 'tasks.json')
    tasks = load_json_file(tasks_file)
    minimum, maximum, estimate = get_totals(tasks)
    result = run_simulation(minimum, maximum)
    save_graph(result, estimate)
    table = create_table(result, estimate)
    with open(os.path.join(OUTPUT_DIR, 'table.txt'), 'w') as f:
        print(table, file=f)
    print(table)
