"""Run this script after "task_planner.py" to perform the computation.

You can stop and re-run this script multiple times if needed.
This script support resuming the computations for each bundle completed.


"""
import multiprocessing
import os
import subprocess
from multiprocessing import Queue
from time import sleep

MAX_PROCS_COUNT = multiprocessing.cpu_count() - 1

if not os.path.isdir('results'):
    os.mkdir('results')

procs_running = set()
tasks = Queue()
for task in os.listdir('tasks'):
    tasks.put(task)

# Ensure all CPU cores are always busy.
while not tasks.empty():

    # Detect ended processes.
    proc_to_del = []
    for proc_running in procs_running:
        if not proc_running.poll() is None:
            proc_to_del.append(proc_running)
    for proc_done in proc_to_del:
        procs_running.remove(proc_done)

    # Start new processes if any slot are available.
    if len(procs_running) < MAX_PROCS_COUNT:
        print(f"task_scheduler: run new task...")
        procs_running.add(subprocess.Popen(['python.exe', 'task_runner.py', tasks.get()]))
        print(f"task_scheduler: remaining {tasks.qsize()} tasks.")
    else:
        sleep(5)

# Ensure all processes has ended
while len(procs_running) > 0:
    proc_to_del = []
    for proc_running in procs_running:
        proc_running.poll()
        if proc_running.returncode is not None:
            proc_to_del.append(proc_running)

    for proc_done in proc_to_del:
        procs_running.remove(proc_done)