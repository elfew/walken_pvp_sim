"""Used initially but not fast enought to simulate multiple scenario.

Bottlenecked probably by the usage of random functions.
"""

import statistics
from multiprocessing import Queue
from random import randint

from walken_pvp_sim.score import Cathlete, Discipline, compute_battle_score


def _print_stats(scores):
    scores.sort()
    print(
        f"Score: {min(scores):.2f} - {max(scores):.2f} (median: {statistics.median(scores):.2f})")


def sim_score_range(cathlete, myberry_boost):
    sim_score_urban = []
    for x in range(0, 1000000):
        sim_score_urban.append(compute_battle_score(cathlete, Discipline.URBAN, myberry_boost))
    sim_score_marathon = []

    for x in range(0, 1000000):
        sim_score_marathon.append(compute_battle_score(cathlete, Discipline.MARATHON, myberry_boost))

    sim_score_sprint = []
    for x in range(0, 1000000):
        sim_score_sprint.append(compute_battle_score(cathlete, Discipline.SPRINT, myberry_boost))

    print(f"* {Discipline.URBAN.name}")
    _print_stats(sim_score_urban)

    print(f"* {Discipline.MARATHON.name}")
    _print_stats(sim_score_marathon)

    print(f"* {Discipline.SPRINT.name}")
    _print_stats(sim_score_sprint)


def sim_fight(cat1, cat2, boost, count=10000000):
    history_discipline = []
    win_history = []
    for x in range(0, count):
        discipline = Discipline(randint(1, 3) - 1)
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
    myberry_boost = 30
    cathlete_1 = Cathlete(78.6, 46.8, 108.6)
    cathlete_2 = Cathlete(78, 80.4, 75.6)

    print(f"---- CATHLETE 1 ---- {cathlete_1}")
    sim_score_range(cathlete_1, myberry_boost)
    print("")

    print(f"---- CATHLETE 2 ---- {cathlete_2}")
    sim_score_range(cathlete_2, myberry_boost)
    print("")

    matches_count = 1000000
    print(f"---- {cathlete_1} vs {cathlete_2} ---- ({format(matches_count,',')} PvP matches)")
    sim_fight(cathlete_1, cathlete_2, myberry_boost, matches_count)


if __name__ == "__main__":
    main()