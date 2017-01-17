from database.main import session
from models.spells.spell_buffs import BuffSchema
from utils.helper import parse_int
from models.spells.spell_dots import DotSchema
from models.spells.paladin_spells_template import PaladinSpellsSchema


def load_buff(buff_id: int) -> 'BeneficialBuff':
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
    buff: BuffSchema = session.query(BuffSchema).get(buff_id)
    return buff.convert_to_beneficial_buff_object()


def load_dot(dot_id: int, caster_level: int) -> 'DoT':
    """
    Loads a DoT from the spell_dots table, whose contents are the following:
    Load the information about the DoT, convert it to an instance of class DoT and return it.
    :param dot_id: the entry of the DoT in the spell_dots table
    :param level: the level of the caster
    """
    dot_info: DotSchema = session.query(DotSchema).get(dot_id)

    return dot_info.convert_to_dot_object(caster_level)


def load_paladin_spells_for_level(level: int) -> ['PaladinSpell']:
    """
    Load all the paladin spells that are available for the SPECIFIC level.
    Get all the PaladinSpells schema objects and convert them to PaladinSpell objects.
    Return said objects in a list
    """
    loaded_spells: [PaladinSpellsSchema] = session.query(PaladinSpellsSchema).filter_by(level_required=level).all()

    return [spell.convert_to_paladin_spell_object() for spell in loaded_spells]
