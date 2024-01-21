"""Use this script to generate tasks for be run in // fashion.
"""

import csv
import os
from os import path

from gen import generate_matchups

if not path.isdir('tasks'):
    os.mkdir('tasks')


BUNDLE_SIZE = 10

try:
    match_iter = iter(generate_matchups())
    count = 1
    task_id = 1

    while True:
        with open(f'tasks/task_{task_id}.csv', 'w', newline='') as task_file:
            task_csvwriter = csv.writer(task_file)
            while count <= BUNDLE_SIZE:
                task_csvwriter.writerow(next(match_iter))
                count = count + 1
        task_id = task_id + 1
        count = 0
except StopIteration:
    pass
