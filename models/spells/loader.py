from database.main import session
from models.spells.spell_buffs import Buff
from loader import parse_int
from models.spells.spell_dots import Dot as DotSchema
from buffs import BeneficialBuff, DoT
from damage import Damage


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


def load_dot(dot_id: int, caster_level: int) -> DoT:
    """
    Loads a DoT from the spell_dots table, whose contents are the following:
    Load the information about the DoT, convert it to an instance of class DoT and return it.
    :param dot_id: the entry of the DoT in the spell_dots table
    :param level: the level of the caster
    """
    dot_info: DotSchema = session.query(DotSchema).get(dot_id)

    dot_name: str = dot_info.name
    dot_damage_per_tick: int = dot_info.damage_per_tick
    dot_damage_school: str = dot_info.damage_school
    dot_duration: int = dot_info.duration

    if dot_damage_school == "magic":
        dot_damage: Damage = Damage(magic_dmg=dot_damage_per_tick)
    elif dot_damage_school == "physical":
        dot_damage: Damage = Damage(phys_dmg=dot_damage_per_tick)
    else:
        raise Exception('Unsupported Damage type!')

    return DoT(name=dot_name, damage_tick=dot_damage, duration=dot_duration, caster_lvl=caster_level)
