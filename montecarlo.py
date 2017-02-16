import random
import json
import matplotlib.pyplot as plt
from collections import OrderedDict

SIMULATION_RUN_COUNT = 500

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
    for task in tasks:
        minimum += task["minimum"]
        maximum += task["maximum"]
    return minimum, maximum


def run_simulation(minimum, maximum):
    '''
    Runs the simulation and returns the result
    '''
    results = []
    sim_result = OrderedDict()

    for time in range(minimum, maximum + 1):
        sim_result[time] = {"number": 0}

    for i in range(SIMULATION_RUN_COUNT):
        value = random.randint(minimum, maximum)
        for key in range(value, maximum +1):
            sim_result[key]["number"] += 1

    for result in sim_result.values():
        result["percentage"] = int((result["number"] / SIMULATION_RUN_COUNT) * 100)

    return sim_result


def save_graph(result):
    '''
    Plots and then saves graph of results
    '''
    fig, ax = plt.subplots()
    ax.barh(list(result.keys()), [sim_result["percentage"] for sim_result in result.values()], color='r')

    plt.xlabel('Percentage')
    plt.ylabel('Time')
    plt.gca().invert_yaxis()
    plt.savefig('chart.png')


def create_table(result):
    '''
    Saves a pretty printed table output of the results
    '''
    try:
        from prettytable import PrettyTable
        table = PrettyTable()
        table.add_column("Time", list(result.keys()))
        table.add_column("Number of times (Out of {})".format(SIMULATION_RUN_COUNT), [sim_result["number"] for sim_result in result.values()])
        table.add_column("Percent of total (rounded)", [sim_result["percentage"] for sim_result in result.values()])
        with open('table.txt', 'w') as f:
            print(table, file=f)
        return table
    except ImportError:
        print("No pretty table as module not installed.\n See table.txt for previuosly generated example")


if __name__ == '__main__':
    tasks_file = 'data.json'
    tasks = load_json_file(tasks_file)
    minimum, maximum = get_totals(tasks)
    result = run_simulation(minimum, maximum)
    save_graph(result)
    table = create_table(result)
    print(table)
