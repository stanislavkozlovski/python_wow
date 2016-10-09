# Short summary of past TODOs
- [x] Add Creatures
- [x] Add Combat
- [x] Add Character Death
- [x] Add an Experience System
- [x] Add Levels
- [x] Add a "?" command that displays all the available commands
- [x] Add a class to the game. (added Paladin)
- [x] Add spells to a certain class. (added Paladin spells)
- [x] Add Quests
- [x] Add currency to the game
- [x] Add items to the game
- [x] Add loot to monsters
- [x] Add Friendly NPCs
- [x] Add stack functionability to the items
- [x] Add zones to the game
- [x] Add vendors to the game
- [x] Move these TODOs to a separate file!
- [x] Print own inventory
- [x] Print NPCs
- [x] Remove the int() calls from loader.py
- [x] Add ability for player to equip weapons and eventually other items
- [x] Convert the damage into it's own separate class.
- [x] Add magic damage
- [x] Add Quests that require items
- [x] Refactor function parameter names in the command_handler and information_printer modules
- [x] Add Buffs to the game
- [x] Add Potions to the game
- [x] Create a spell_dots DB table and load dot information from there. Somehow link that table to paladin_spells_template
- [x] Add DoTs to the game
- [x] Move the logic that checks if a player can learn a new spell into it's own method!
- [x] Move the logic that checks if a monster is dead in combat.py to a separate function. This will fix a bug where if a monster dies from a DoT, the loot is not shown after the player enters a command.
- [x] Move the logic that checks for buff's/dot's expiry in the start/end turn method of LivingEntity to their own methods.
- [x] Create a method in Character that calculates the level difference damage reduction/increase and apply it to DoTs
- [x] Print in colors
- [x] Refactor Buff classes, make Buff a base class for all kinds of buffs/dots/debuffs
- [x] Convert heals into their own separate class.
- [x] Add Quest item rewards
- [x] Fix a bug in fetch quests where they don't remove their required items from your inventory
- [x] Add command to print item information (that is in the vendor dialogue)
- [x] Add "take all" command when looting creatures to take all the loot at once.
- [x] Add Holyheal
- [x] Add ProtectiveHeal
- [x] Add spell cooldowns and a way to handle them
- [x] Store player's attributes (mana,hp etc) in a dictionary (easier application of buffs that way, will remove if checks)
- [x] Add entry to A Peculiar Hut possible only if you've killed Garrick Padfoot
- [x] Add scripted event (brotherhood traitors talking) in A Peculiar Hut
- [x] Monster gossip on attack
- [x] Add armor to monsters
- [x] Sell option to sell items to vendors
- [x] Add the ability to save the character
- [x] List all saved characters when the user wants to load a character

# Low Priority TODOs
- Add more content(monster, zone/subzones, npcs, items, vendors, spells and etc)
- Add list with last twenty prints, clear the console and rewrite again whenever a command has been added
- Add Talents System

# Small TODOs
- Print Equipment
- Print Stats (hp, mana, xp and everything else at once)
- Add item gossip text
- Fix bug where when we attack a monster, the monster's absorption does not get printed.
- Move the functions that choose what to do based on the user's command to a new module, something like command_router, which will route appropriate commands to their handlers in command_handler.py


# TODOs
- Add documentation!
- Add some kind of armor item type (Head, etc)
- Add another class of choice. (Mage is on my mind)


- Add a scripted NPC to the game

- Implement HoTs (heal over time effects)
- Add NatureHeal
- Create one shared creature_default DB table holding all the default values for creatures at a certain level (gold, xp, armor)
- Add different kinds of damage
- Create more damage classes, each with it's own flavour. (Destruction leaves off a DoT, Sinister has a chance to strike again, Merciless has a chance to crit and others without flavor (holy, frost, fire etc))
