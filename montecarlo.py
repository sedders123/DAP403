import random
import json
import matplotlib.pyplot as plt

SIMULATION_RUN_TIMES = 500


def get_totals(tasks):
    maximum = 0
    minimum = 0
    for task in tasks:
        minimum += task["minimum"]
        maximum += task["maximum"]
    return minimum, maximum


def get_result(minimum, maximum):
    results = []
    for i in range(SIMULATION_RUN_TIMES):
        results.append(random.randint(minimum, maximum))
    sim_result = {}
    for i in range(minimum, maximum + 1):
        sim_result[i] = {"number": 0}

    for result in results:
        for key in range(result, maximum + 1):
            sim_result[key]["number"] += 1

    percentages = []
    for key, result in sim_result.items():
        result["percentage"] = int((result["number"] / SIMULATION_RUN_TIMES) * 100)
        percentages.append(result["percentage"])

    return sim_result, percentages


def save_graph(result, percentages):
    fig, ax = plt.subplots()
    ax.barh(list(result.keys()), list(percentages), color='r')

    plt.xlabel('Percentage')
    plt.ylabel('Time')
    plt.gca().invert_yaxis()
    plt.savefig('chart.png')


def create_table(result, percentages):
    try:
        from prettytable import PrettyTable
        table = PrettyTable()
        table.add_column("Time", list(result.keys()))
        table.add_column(f"Number of times (Out of {SIMULATION_RUN_TIMES})", [sim_result["number"] for sim_result in result.values()])
        table.add_column("Percent of total (rounded)", percentages)
        with open('table.txt', 'w') as f:
            print(table, file=f)
        return table
    except ImportError:
        print("No pretty table as module not installed.\n See table.txt for previuosly generated example")


def load_tasks():
    with open('data.json') as data_file:
        tasks = json.load(data_file)
    return tasks


if __name__ == '__main__':
    tasks = load_tasks()
    minimum, maximum = get_totals(tasks)
    result, percentages = get_result(minimum, maximum)
    save_graph(result, percentages)
    table = create_table(result, percentages)
    print(table)
