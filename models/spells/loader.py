from database.main import session
from models.spells.spell_buffs import Buff
from loader import parse_int
from buffs import BeneficialBuff


def load_buff(buff_id: int) -> BeneficialBuff:
    """
    Loads a buff from the DB table spells_buffs, whose contents are the following:
    entry,             name, duration,    stat,   amount,   stat2,   amount2,stat3,   amount3, comment
        1,  Heart of a Lion,        5,strength,       10,                                      Increases strength by 10 for 5 turns
        stat - the stat this buff increases
        amount - the amount it increases the stat by
        duration - the amount of turns this buff lasts for
    This buff increases your strength by 10 for 5 turns.

    Load the information about the buff, convert it to an class Buff object and return it
    :param buff_id: the buff entry in spells_buffs
    :return: A instance of class Buff
    """
    buff_info = session.query(Buff).get(buff_id)
    buff_name: str = buff_info.name
    buff_stat1: str = buff_info.stat1
    buff_amount1: int = parse_int(buff_info.amount1)
    buff_stat2: str = buff_info.stat2
    buff_amount2: int = parse_int(buff_info.amount2)
    buff_stat3: str = buff_info.stat3
    buff_amount3: int = parse_int(buff_info.amount3)
    buff_duration: int = parse_int(buff_info.duration)

    buffs: [tuple] = [(buff_stat1, buff_amount1), (buff_stat2, buff_amount2), (buff_stat3, buff_amount3)]

    return BeneficialBuff(name=buff_name, buff_stats_and_amounts=buffs,
                          duration=buff_duration)
