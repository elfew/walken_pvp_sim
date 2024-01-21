import csv

from walken_pvp_sim.gen import generate_matchups

# ANALYSYS
# ---------
matches_computed = set()
with open(f'results/AllResults.csv', 'r') as result_file:
    results = csv.reader(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for result in results:
        matches_computed.add(((int(result[0]), int(result[1]), int(result[2])),(int(result[3]), int(result[4]), int(result[5]))))
print(f"Computed: {len(matches_computed)}")

missed_matches = []

matches_todo = set(generate_matchups())
print(f"Possibilities: {len(matches_todo)}")
for x in matches_todo.difference(matches_computed):
    missed_matches.append(x)

print(f"Missing: {len(missed_matches)}")

match_by_build = {}
for a, b in matches_todo:
    match_by_build[a] = match_by_build.get(a, 0) + 1

for k, v in match_by_build.items():
    print(f"build: {k} - encounters: {v}")


# PLANNER
# ---------
BUNDLE_SIZE = 5

try:
    match_iter = iter(missed_matches)
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