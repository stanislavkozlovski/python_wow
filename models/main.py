# Import every model out there to load the model itself
from models.items import (item_template, loot_table)
from models.misc import (level_xp_requirement, levelup_stats)
from models.quests import quest_template
from models.creatures.creature_defaults import creature_defaults
from models.creatures import (npc_vendor, creature_template, creatures)
from models.characters import saved_character
from models.spells import (paladin_spells_template, spell_dots, spell_buffs)
# WARNING: The order of which everything is imported is crucial!
