import random
import matplotlib.pyplot as plt

SIMULATION_RUN_TIMES = 500

job1 = {
    "name": "job1",
    "estimate": 5,
    "minimum": 4,
    "maximum": 7
}
job2 = {
    "name": "job2",
    "estimate": 4,
    "minimum": 3,
    "maximum": 6
}
job3 = {
    "name": "job3",
    "estimate": 5,
    "minimum": 4,
    "maximum": 6
}

tasks = [job1, job2, job3]
results = []

total = {
    "minimum": 0,
    "maximum": 0
}

for task in tasks:
    total["minimum"] += task["minimum"]
    total["maximum"] += task["maximum"]

results = []

for i in range(SIMULATION_RUN_TIMES):
    results.append(random.randint(total["minimum"], total["maximum"]))

sim_result = {}
for i in range(total["minimum"], total["maximum"] + 1):
    sim_result[i] = {"number": 0}

for result in results:
    for key in range(result, total["maximum"]+1):
        sim_result[key]["number"] += 1

percentages = []

for key, result in sim_result.items():
    result["percentage"] = int((result["number"] / SIMULATION_RUN_TIMES) * 100)
    percentages.append(result["percentage"])

fig, ax = plt.subplots()
ax.barh(list(sim_result.keys()), list(percentages), color='r')

plt.xlabel('Percentage')
plt.ylabel('Time')
plt.gca().invert_yaxis()
plt.savefig('myfig.png')

try:
    from prettytable import PrettyTable
    table = PrettyTable()
    table.add_column("Time", list(sim_result.keys()))
    table.add_column(f"Number of times (Out of {SIMULATION_RUN_TIMES})", [result["number"] for result in sim_result.values()])
    table.add_column("Percent of total (rounded)", percentages)
    print(table)
    with open('table.txt', 'w') as f:
        print(table, file=f)
except ImportError:
    print("No pretty table as module not installed.\n See table.txt for previuosly generated example")
