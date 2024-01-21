"""PvP score computations.
"""
import random
from enum import IntEnum


class Cathlete:
    def __init__(self, strength, endurance, speed):
        self.speed = speed
        self.endurance = endurance
        self.strength = strength

    @property
    def cathletism(self):
        return self.speed + self.endurance + self.strength

    def __str__(self):
        return "{}/{}/{} (cathletism: {:.2f})".format(self.strength, self.endurance, self.speed, self.cathletism)

class Discipline(IntEnum):
    URBAN = 0,
    MARATHON = 1,
    SPRINT = 2



def compute_urban_raw(strength, endurance, speed):
    return 1 * strength + 0.5 * endurance + 0.5 * speed


def compute_marathon_raw(strength, endurance, speed):
    return 0.25 * strength + 1 * endurance + 0.25 * speed


def compute_sprint_raw(strength, endurance, speed):
    return 0.5 * strength + 0.25 * endurance + 1 * speed


def get_buff_msb(strength, endurance, speed, msb_buff: float):
    """"""
    target = random.randint(1,3)
    if target == 1:
        return strength * (msb_buff / 100), 0, 0
    elif target == 2:
        return 0, endurance * (msb_buff / 100), 0
    else:
        return 0, 0, speed * (msb_buff / 100)


def get_buff_milk(strength, endurance, speed):

    # Seems the game just spread a total of 30% milk across all stats.
    total = 30
    buff1 = random.randint(3, 20)
    buff2 = random.randint(3, min(20, (total-buff1-3)))
    buff3 = total - buff1 - buff2

    assert (buff1+buff2+buff3 == 30)

    return strength * buff1 / 100, endurance * buff2 / 100, speed * buff3 / 100


def get_debuff_laser() -> float:
    return random.randint(3, 20)


def compute_battle_score(cathlete: Cathlete, discipline: Discipline, myberry_boost: float):
    fn_compute = [compute_urban_raw, compute_marathon_raw, compute_sprint_raw]

    buff_msb_str, buff_msb_end, buff_msb_spd = get_buff_msb(cathlete.strength, cathlete.endurance, cathlete.speed,
                                                            myberry_boost)
    buff_milk_str, buff_milk_end, buff_milk_spd = get_buff_milk(cathlete.strength, cathlete.endurance, cathlete.speed)
    debuff_laser = get_debuff_laser()
    # print(f'laser: -{debuff_laser}')
    score = fn_compute[discipline.value](cathlete.strength + buff_msb_str + buff_milk_str,
                                          cathlete.endurance + buff_msb_end + buff_milk_end,
                                          cathlete.speed + buff_msb_spd + buff_milk_spd)
    return score - (100/score * debuff_laser)

