import itertools


def generate_builds():
    cathletism = 234

    min_stat = 44
    max_stat = cathletism - min_stat * 2
    step = 10

    stat_str_range = list(range(min_stat, max_stat, step))
    builds = set()
    for stat_str in stat_str_range:
        stat_sta_range = list(range(min_stat, cathletism - stat_str - min_stat, step))

        for stat_sta in stat_sta_range:
            stat_spd = cathletism - stat_str - stat_sta
            # print(f"{stat_str},{stat_sta},{stat_spd} = {stat_str + stat_sta + stat_spd}")
            builds.add((stat_str, stat_sta, stat_spd))
    return builds


def generate_matchups():
    cathletes = generate_builds()
    print(f"Builds: {len(cathletes)}")
    matchups = set(itertools.product(cathletes, repeat=2))
    print(f"Matchups: {len(matchups)}")
    return matchups
