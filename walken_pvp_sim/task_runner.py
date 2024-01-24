# Ensure the venv is enabled. This is started in its own interpreter.
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
this_project_dir = os.path.join(this_dir, os.pardir)
activate_this_path = os.path.join(this_project_dir, r'.venv\Scripts\activate_this.py')
exec(open(activate_this_path).read(),
     {'__file__': activate_this_path})
#########################################################################

"""(Do not run) This script handle computation from a text file specified as argument.
"""
import csv
import datetime
import os
import sys
import time
from ast import literal_eval as make_tuple
from multiprocessing import Queue

from walken_pvp_sim.score import Cathlete, Discipline, compute_battle_score, generator


def sim_fight(cat1, cat2, boost):
    history_discipline = []
    win_history = []
    for x in range(0, 1000000):
        discipline = Discipline(generator.integers(1, 3, endpoint=True) - 1)
        cat1_score = compute_battle_score(cat1, discipline, boost)
        cat2_score = compute_battle_score(cat2, discipline, boost)
        if cat1_score > cat2_score:
            win_history.append(1)
        elif cat2_score > cat1_score:
            win_history.append(2)
        else:
            win_history.append(0)
        history_discipline.append(discipline)
    print(f"* CAT 1 win: {win_history.count(1)} ({(100 / len(win_history) * win_history.count(1)):.5f} %)")
    print(f"* CAT 2 win: {win_history.count(2)} ({(100 / len(win_history) * win_history.count(2)):.5f} %)")
    print(f"* No winner : {win_history.count(0)} ({(100 / len(win_history) * win_history.count(0)):.5f} %)")

    print(
        f"urban: {history_discipline.count(Discipline.URBAN)} / marathon: {history_discipline.count(Discipline.MARATHON)} / sprint : {history_discipline.count(Discipline.SPRINT)}")

    return (win_history.count(1), win_history.count(2), win_history.count(3),
            history_discipline.count(Discipline.URBAN),
            history_discipline.count(Discipline.MARATHON),
            history_discipline.count(Discipline.SPRINT))


def worker(tasks: Queue, results: Queue):
    while not tasks.empty():
        build1, build2 = tasks.get()
        cat1 = Cathlete(*build1)
        cat2 = Cathlete(*build2)
        cat1_win, cat2_win, tie, urban, marathon, sprint = sim_fight(cat1, cat2, 30)
        results.put([
                    cat1.strength, cat1.endurance, cat1.speed,
                    cat2.strength, cat2.endurance, cat2.speed,
                    cat1_win, cat2_win, tie,
                    urban, marathon, sprint
                    ])


def main():
    task_fname = sys.argv[1]
    print(f"Working on : {task_fname}...")

    matchs = []
    with open(f"tasks/{task_fname}", 'r') as task_file:
        result_reader = csv.reader(task_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for build1, build2 in result_reader:
            matchs.append((make_tuple(build1), make_tuple(build2)))

    todo_count = len(matchs)
    done = 1

    results = []
    for build1, build2 in matchs:
        start_time = time.time()
        cat1 = Cathlete(*build1)
        cat2 = Cathlete(*build2)

        cat1_win, cat2_win, tie, urban, marathon, sprint = sim_fight(Cathlete(*build1), Cathlete(*build2), boost=30)

        results.append([
                cat1.strength, cat1.endurance, cat1.speed,
                cat2.strength, cat2.endurance, cat2.speed,
                cat1_win, cat2_win, tie,
                urban, marathon, sprint
            ])

        elapsed = (time.time() - start_time)
        print(f"{task_fname}: Elapsed : {elapsed:.2f} seconds ---")
        now = datetime.datetime.now()
        end_date = now + datetime.timedelta(0, elapsed * (todo_count - done))
        print(f"{task_fname}: Completion ETA {end_date} ({done}/{todo_count})")
        done = done + 1

        # print(build1)
        # print(build2)
        # sim_fight(Cathlete(*build1), Cathlete(*build2), myberry_boost)
    # print("---- CATHELTE 1 vs CATHLETE 2 ----")
    # sim_fight(cathlete_1, cathlete_2, myberry_boost)

    with open(f'results/{task_fname}', 'w', newline='') as result_file:
        result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # result_writer.writerow(
        #     ['cat1_str', 'cat1_end', 'cat1_spd', 'cat2_str', 'cat2_end', 'cat2_spd', 'cat1_win', 'cat2_win', 'tie', 'urban',
        #      'marathon', 'sprint'])
        result_writer.writerows(results)

    os.unlink(f"tasks/{task_fname}")

if __name__ == "__main__":
    main()
