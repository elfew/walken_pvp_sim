"""Use this script to generate tasks for be run in // fashion.
"""

import csv
import multiprocessing
import os
from datetime import timedelta
from os import path

from gen import generate_matchups, generate_builds

if not path.isdir('tasks'):
    os.mkdir('tasks')


BUNDLE_SIZE = 10

# for estimation of duration:
TIME_PER_BUNDLE_IN_SECS = 9 * 60
WORKER_COUNT = multiprocessing.cpu_count() - 1

try:
    builds = tuple(generate_builds(stat_min=45, stat_max=120, stat_step=5, cathletism=234))
    matchups = tuple(generate_matchups(builds))
    print(f"Generating : {format(len(matchups), ",")} encounters (builds: {format(len(builds), ",")})")
    duration_seconds = len(matchups) / BUNDLE_SIZE * TIME_PER_BUNDLE_IN_SECS / WORKER_COUNT
    print(f"Processing time (ETA) : {timedelta(seconds=duration_seconds)}")

    count = 0
    task_id = 1

    matchups = iter(matchups)
    while True:
        with open(f'tasks/task_{task_id}.csv', 'w', newline='') as task_file:
            task_csvwriter = csv.writer(task_file)
            while count < BUNDLE_SIZE:
                task_csvwriter.writerow(next(matchups))
                count = count + 1
        task_id = task_id + 1
        count = 0
except StopIteration:
    pass
