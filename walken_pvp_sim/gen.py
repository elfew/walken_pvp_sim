import itertools


def generate_builds(stat_min, stat_step, stat_max, cathletism):
    """Generate cathletes builds."""
    for stat_str, stat_stam in itertools.product(range(stat_min, cathletism + 1, stat_step), repeat=2):
        stat_spd = cathletism - stat_str - stat_stam

        if (stat_str + stat_stam <= cathletism
                and stat_str < stat_max
                and stat_stam < stat_max
                and stat_min < stat_spd < stat_max):
            yield stat_str, stat_stam, stat_spd


def generate_matchups(builds):
    """Generate encounters between builds."""
    return itertools.product(builds, repeat=2)
