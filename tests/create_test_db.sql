--
-- File generated with SQLiteStudio v3.1.0 on вт ян. 17 16:50:48 2017
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: quest_template
DROP TABLE IF EXISTS quest_template;

CREATE TABLE quest_template (
    entry               INTEGER      PRIMARY KEY AUTOINCREMENT,
    name                VARCHAR (60),
    type                VARCHAR (60),
    level_required      INTEGER,
    monster_required    VARCHAR (60),
    item_required       VARCHAR (60),
    amount_required     INTEGER,
    zone                VARCHAR (60),
    sub_zone            VARCHAR (60),
    xp_reward           INTEGER,
    comment             TEXT,
    item_reward1        INTEGER,
    item_reward2        INTEGER,
    item_reward3        INTEGER,
    item_choice_enabled INTEGER      NOT NULL
                                     DEFAULT (0) 
);

INSERT INTO quest_template (
                               entry,
                               name,
                               type,
                               level_required,
                               monster_required,
                               item_required,
                               amount_required,
                               zone,
                               sub_zone,
                               xp_reward,
                               comment,
                               item_reward1,
                               item_reward2,
                               item_reward3,
                               item_choice_enabled
                           )
                           VALUES (
                               1,
                               'A Canine Menace',
                               'killquest',
                               1,
                               'Wolf',
                               NULL,
                               5,
                               'Northshire Abbey',
                               'Northshire Valley',
                               300,
                               'Kill 5 wolves',
                               NULL,
                               NULL,
                               NULL,
                               ''
                           );

INSERT INTO quest_template (
                               entry,
                               name,
                               type,
                               level_required,
                               monster_required,
                               item_required,
                               amount_required,
                               zone,
                               sub_zone,
                               xp_reward,
                               comment,
                               item_reward1,
                               item_reward2,
                               item_reward3,
                               item_choice_enabled
                           )
                           VALUES (
                               2,
                               'Canine-Like Hunger',
                               'fetchquest',
                               1,
                               '',
                               'Wolf Meat',
                               2,
                               'Northshire Abbey',
                               'Northshire Valley',
                               300,
                               'Obtain 2 Wolf Meats',
                               1,
                               4,
                               NULL,
                               1
                           );

INSERT INTO quest_template (
                               entry,
                               name,
                               type,
                               level_required,
                               monster_required,
                               item_required,
                               amount_required,
                               zone,
                               sub_zone,
                               xp_reward,
                               comment,
                               item_reward1,
                               item_reward2,
                               item_reward3,
                               item_choice_enabled
                           )
                           VALUES (
                               3,
                               'Bounty on Garrick Padfoot',
                               'fetchquest',
                               3,
                               '',
                               'Garrick''s Head',
                               1,
                               'Northshire Abbey',
                               'Northshire Vineyards',
                               500,
                               'Kill Combat Garrick Padfoot and bring his head as proof',
                               NULL,
                               NULL,
                               NULL,
                               ''
                           );


-- Table: saved_character
DROP TABLE IF EXISTS saved_character;

CREATE TABLE saved_character (
    name                VARCHAR (60) UNIQUE
                                     PRIMARY KEY,
    class               VARCHAR (60),
    level               INTEGER,
    loaded_scripts_ID   INTEGER,
    killed_monsters_ID  INTEGER,
    completed_quests_ID INTEGER,
    equipment_ID        INTEGER,
    inventory_ID        INTEGER,
    gold                INTEGER
);

INSERT INTO saved_character (
                                name,
                                class,
                                level,
                                loaded_scripts_ID,
                                killed_monsters_ID,
                                completed_quests_ID,
                                equipment_ID,
                                inventory_ID,
                                gold
                            )
                            VALUES (
                                'Netherblood',
                                'paladin',
                                3,
                                1,
                                1,
                                1,
                                1,
                                1,
                                24
                            );


-- Table: spell_dots
DROP TABLE IF EXISTS spell_dots;

CREATE TABLE spell_dots (
    entry           INTEGER      PRIMARY KEY AUTOINCREMENT,
    name            VARCHAR (60),
    damage_per_tick INTEGER,
    damage_school   VARCHAR (60),
    duration        INTEGER,
    comment         TEXT
);

INSERT INTO spell_dots (
                           entry,
                           name,
                           damage_per_tick,
                           damage_school,
                           duration,
                           comment
                       )
                       VALUES (
                           1,
                           'Melting',
                           2,
                           'magic',
                           2,
                           'Melting Strike RANK 1'
                       );


-- Table: saved_character_completed_quests
DROP TABLE IF EXISTS saved_character_completed_quests;

CREATE TABLE saved_character_completed_quests (
    id         INTEGER,
    quest_name STRING
);


-- Table: saved_character_inventory
DROP TABLE IF EXISTS saved_character_inventory;

CREATE TABLE saved_character_inventory (
    id         INTEGER,
    item_id    INTEGER,
    item_count INTEGER
);

INSERT INTO saved_character_inventory (
                                          id,
                                          item_id,
                                          item_count
                                      )
                                      VALUES (
                                          2,
                                          300,
                                          3
                                      );

INSERT INTO saved_character_inventory (
                                          id,
                                          item_id,
                                          item_count
                                      )
                                      VALUES (
                                          1,
                                          11,
                                          5
                                      );

INSERT INTO saved_character_inventory (
                                          id,
                                          item_id,
                                          item_count
                                      )
                                      VALUES (
                                          1,
                                          1,
                                          1
                                      );

INSERT INTO saved_character_inventory (
                                          id,
                                          item_id,
                                          item_count
                                      )
                                      VALUES (
                                          1,
                                          2,
                                          1
                                      );


-- Table: spell_buffs
DROP TABLE IF EXISTS spell_buffs;

CREATE TABLE spell_buffs (
    entry    INTEGER      PRIMARY KEY AUTOINCREMENT,
    name     VARCHAR (60),
    duration INTEGER,
    stat1    VARCHAR (60),
    amount1  INTEGER,
    stat2    VARCHAR (60),
    amount2  INTEGER,
    stat3    VARCHAR (60),
    amount3  INTEGER,
    comment  TEXT
);

INSERT INTO spell_buffs (
                            entry,
                            name,
                            duration,
                            stat1,
                            amount1,
                            stat2,
                            amount2,
                            stat3,
                            amount3,
                            comment
                        )
                        VALUES (
                            1,
                            'Heart of a Lion',
                            5,
                            'strength',
                            15,
                            NULL,
                            NULL,
                            NULL,
                            NULL,
                            'HAH EI BOKLUK5 for 5 turns'
                        );


-- Table: saved_character_killed_monsters
DROP TABLE IF EXISTS saved_character_killed_monsters;

CREATE TABLE saved_character_killed_monsters (
    id   INTEGER,
    GUID INTEGER
);

INSERT INTO saved_character_killed_monsters (
                                                id,
                                                GUID
                                            )
                                            VALUES (
                                                1,
                                                20
                                            );

INSERT INTO saved_character_killed_monsters (
                                                id,
                                                GUID
                                            )
                                            VALUES (
                                                1,
                                                15
                                            );


-- Table: saved_character_loaded_scripts
DROP TABLE IF EXISTS saved_character_loaded_scripts;

CREATE TABLE saved_character_loaded_scripts (
    id          INTEGER,
    script_name TEXT
);

INSERT INTO saved_character_loaded_scripts (
                                               id,
                                               script_name
                                           )
                                           VALUES (
                                               2,
                                               'ss'
                                           );

INSERT INTO saved_character_loaded_scripts (
                                               id,
                                               script_name
                                           )
                                           VALUES (
                                               2,
                                               'brr'
                                           );

INSERT INTO saved_character_loaded_scripts (
                                               id,
                                               script_name
                                           )
                                           VALUES (
                                               1,
                                               'HASKEL_PAXTON_CONVERSATION'
                                           );


-- Table: paladin_spells_template
DROP TABLE IF EXISTS paladin_spells_template;

CREATE TABLE paladin_spells_template (
    id             INTEGER      PRIMARY KEY AUTOINCREMENT,
    name           VARCHAR (60),
    rank           INTEGER,
    level_required INTEGER,
    damage1        INTEGER,
    damage2        INTEGER,
    damage3        INTEGER,
    heal1          INTEGER,
    heal2          INTEGER,
    heal3          INTEGER,
    mana_cost      INTEGER,
    effect         INTEGER,
    cooldown       INTEGER,
    comment        TEXT
);

INSERT INTO paladin_spells_template (
                                        id,
                                        name,
                                        rank,
                                        level_required,
                                        damage1,
                                        damage2,
                                        damage3,
                                        heal1,
                                        heal2,
                                        heal3,
                                        mana_cost,
                                        effect,
                                        cooldown,
                                        comment
                                    )
                                    VALUES (
                                        1,
                                        'Seal of Righteousness',
                                        1,
                                        1,
                                        2,
                                        0,
                                        0,
                                        0,
                                        0,
                                        0,
                                        4,
                                        NULL,
                                        NULL,
                                        NULL
                                    );

INSERT INTO paladin_spells_template (
                                        id,
                                        name,
                                        rank,
                                        level_required,
                                        damage1,
                                        damage2,
                                        damage3,
                                        heal1,
                                        heal2,
                                        heal3,
                                        mana_cost,
                                        effect,
                                        cooldown,
                                        comment
                                    )
                                    VALUES (
                                        2,
                                        'Seal of Righteousness',
                                        2,
                                        3,
                                        4,
                                        0,
                                        0,
                                        0,
                                        0,
                                        0,
                                        6,
                                        NULL,
                                        NULL,
                                        NULL
                                    );

INSERT INTO paladin_spells_template (
                                        id,
                                        name,
                                        rank,
                                        level_required,
                                        damage1,
                                        damage2,
                                        damage3,
                                        heal1,
                                        heal2,
                                        heal3,
                                        mana_cost,
                                        effect,
                                        cooldown,
                                        comment
                                    )
                                    VALUES (
                                        3,
                                        'Flash of Light',
                                        1,
                                        2,
                                        0,
                                        0,
                                        0,
                                        6,
                                        0,
                                        0,
                                        7,
                                        NULL,
                                        NULL,
                                        'Heals the character'
                                    );

INSERT INTO paladin_spells_template (
                                        id,
                                        name,
                                        rank,
                                        level_required,
                                        damage1,
                                        damage2,
                                        damage3,
                                        heal1,
                                        heal2,
                                        heal3,
                                        mana_cost,
                                        effect,
                                        cooldown,
                                        comment
                                    )
                                    VALUES (
                                        4,
                                        'Melting Strike',
                                        1,
                                        3,
                                        3,
                                        0,
                                        0,
                                        0,
                                        0,
                                        0,
                                        6,
                                        1,
                                        3,
                                        'Damages the target for damage1 and applies a DoT to the target'
                                    );


-- Table: creature_defaults
DROP TABLE IF EXISTS creature_defaults;

CREATE TABLE creature_defaults (
    creature_level  INTEGER PRIMARY KEY,
    armor           INTEGER,
    min_gold_reward INTEGER,
    max_gold_reward INTEGER,
    xp_reward       INTEGER
);

INSERT INTO creature_defaults (
                                  creature_level,
                                  armor,
                                  min_gold_reward,
                                  max_gold_reward,
                                  xp_reward
                              )
                              VALUES (
                                  1,
                                  50,
                                  2,
                                  5,
                                  50
                              );

INSERT INTO creature_defaults (
                                  creature_level,
                                  armor,
                                  min_gold_reward,
                                  max_gold_reward,
                                  xp_reward
                              )
                              VALUES (
                                  2,
                                  65,
                                  4,
                                  6,
                                  75
                              );

INSERT INTO creature_defaults (
                                  creature_level,
                                  armor,
                                  min_gold_reward,
                                  max_gold_reward,
                                  xp_reward
                              )
                              VALUES (
                                  3,
                                  80,
                                  5,
                                  8,
                                  100
                              );

INSERT INTO creature_defaults (
                                  creature_level,
                                  armor,
                                  min_gold_reward,
                                  max_gold_reward,
                                  xp_reward
                              )
                              VALUES (
                                  4,
                                  95,
                                  7,
                                  10,
                                  125
                              );

INSERT INTO creature_defaults (
                                  creature_level,
                                  armor,
                                  min_gold_reward,
                                  max_gold_reward,
                                  xp_reward
                              )
                              VALUES (
                                  5,
                                  110,
                                  9,
                                  12,
                                  150
                              );

INSERT INTO creature_defaults (
                                  creature_level,
                                  armor,
                                  min_gold_reward,
                                  max_gold_reward,
                                  xp_reward
                              )
                              VALUES (
                                  6,
                                  125,
                                  11,
                                  15,
                                  200
                              );

INSERT INTO creature_defaults (
                                  creature_level,
                                  armor,
                                  min_gold_reward,
                                  max_gold_reward,
                                  xp_reward
                              )
                              VALUES (
                                  7,
                                  140,
                                  14,
                                  18,
                                  225
                              );

INSERT INTO creature_defaults (
                                  creature_level,
                                  armor,
                                  min_gold_reward,
                                  max_gold_reward,
                                  xp_reward
                              )
                              VALUES (
                                  8,
                                  155,
                                  16,
                                  20,
                                  250
                              );

INSERT INTO creature_defaults (
                                  creature_level,
                                  armor,
                                  min_gold_reward,
                                  max_gold_reward,
                                  xp_reward
                              )
                              VALUES (
                                  9,
                                  170,
                                  19,
                                  25,
                                  300
                              );

INSERT INTO creature_defaults (
                                  creature_level,
                                  armor,
                                  min_gold_reward,
                                  max_gold_reward,
                                  xp_reward
                              )
                              VALUES (
                                  10,
                                  185,
                                  23,
                                  30,
                                  400
                              );


-- Table: creature_template
DROP TABLE IF EXISTS creature_template;

CREATE TABLE creature_template (
    entry             INTEGER      CONSTRAINT entry PRIMARY KEY AUTOINCREMENT,
    name              VARCHAR (60),
    type              VARCHAR (60),
    level             INTEGER      DEFAULT (1),
    health            INTEGER      DEFAULT (1),
    mana              INTEGER      DEFAULT (1),
    armor             INTEGER      DEFAULT (0),
    min_dmg           INTEGER      DEFAULT (1),
    max_dmg           INTEGER      DEFAULT (2),
    quest_relation_ID INTEGER,
    loot_table_ID     INTEGER,
    gossip            TEXT,
    respawnable       BOOLEAN
);

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  1,
                                  'Adder',
                                  'monster',
                                  1,
                                  3,
                                  0,
                                  0,
                                  1,
                                  2,
                                  NULL,
                                  NULL,
                                  NULL,
                                  1
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  2,
                                  'Foxling',
                                  'monster',
                                  1,
                                  4,
                                  0,
                                  0,
                                  2,
                                  5,
                                  NULL,
                                  NULL,
                                  NULL,
                                  1
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  3,
                                  'Amber Moth',
                                  'monster',
                                  1,
                                  5,
                                  0,
                                  0,
                                  1,
                                  3,
                                  NULL,
                                  NULL,
                                  NULL,
                                  1
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  4,
                                  'Hare',
                                  'monster',
                                  1,
                                  5,
                                  0,
                                  0,
                                  1,
                                  3,
                                  NULL,
                                  NULL,
                                  NULL,
                                  1
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  5,
                                  'Beetle',
                                  'monster',
                                  1,
                                  10,
                                  0,
                                  0,
                                  1,
                                  2,
                                  NULL,
                                  NULL,
                                  NULL,
                                  1
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  6,
                                  'Rat',
                                  'monster',
                                  1,
                                  2,
                                  0,
                                  0,
                                  3,
                                  3,
                                  NULL,
                                  NULL,
                                  NULL,
                                  1
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  7,
                                  'Toad',
                                  'monster',
                                  1,
                                  4,
                                  0,
                                  0,
                                  1,
                                  4,
                                  NULL,
                                  NULL,
                                  NULL,
                                  1
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  8,
                                  'Beggar',
                                  'monster',
                                  2,
                                  8,
                                  0,
                                  0,
                                  2,
                                  4,
                                  NULL,
                                  NULL,
                                  NULL,
                                  1
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  9,
                                  'Bloodtalon Raptor',
                                  'monster',
                                  2,
                                  5,
                                  0,
                                  0,
                                  3,
                                  4,
                                  NULL,
                                  NULL,
                                  NULL,
                                  1
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  10,
                                  'Blue Dragon Turtle',
                                  'monster',
                                  3,
                                  15,
                                  0,
                                  0,
                                  4,
                                  8,
                                  NULL,
                                  NULL,
                                  NULL,
                                  1
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  11,
                                  'Wolf',
                                  'monster',
                                  1,
                                  4,
                                  0,
                                  50,
                                  1,
                                  5,
                                  1,
                                  1,
                                  NULL,
                                  1
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  12,
                                  'Defias Vineyard Crook',
                                  'monster',
                                  2,
                                  12,
                                  0,
                                  80,
                                  2,
                                  4,
                                  NULL,
                                  NULL,
                                  NULL,
                                  1
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  13,
                                  'Lumberjack Joe',
                                  'fnpc',
                                  5,
                                  25,
                                  0,
                                  0,
                                  10,
                                  15,
                                  0,
                                  0,
                                  'Hey there $N, fancy helping me cut down this tree over here?',
                                  1
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  14,
                                  'Meatseller Jack',
                                  'vendor',
                                  4,
                                  20,
                                  0,
                                  0,
                                  5,
                                  10,
                                  0,
                                  0,
                                  'Do you want to buy meat? You''ve come to the right place!',
                                  1
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  15,
                                  'Garrick Padfoot',
                                  'monster',
                                  3,
                                  20,
                                  0,
                                  140,
                                  6,
                                  8,
                                  3,
                                  3,
                                  'I see those fools at the Vineyards sent some fresh meat for us.',
                                  0
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  16,
                                  'Brother Paxton',
                                  'monster',
                                  3,
                                  25,
                                  0,
                                  0,
                                  7,
                                  10,
                                  '',
                                  4,
                                  'Nobody will foil our plans!',
                                  0
                              );

INSERT INTO creature_template (
                                  entry,
                                  name,
                                  type,
                                  level,
                                  health,
                                  mana,
                                  armor,
                                  min_dmg,
                                  max_dmg,
                                  quest_relation_ID,
                                  loot_table_ID,
                                  gossip,
                                  respawnable
                              )
                              VALUES (
                                  17,
                                  'Brother Haskel',
                                  'monster',
                                  3,
                                  30,
                                  0,
                                  0,
                                  7,
                                  10,
                                  '',
                                  '',
                                  'You have not seen the last of us!',
                                  0
                              );


-- Table: npc_vendor
DROP TABLE IF EXISTS npc_vendor;

CREATE TABLE npc_vendor (
    creature_entry INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id        INTEGER,
    item_count     INTEGER DEFAULT (1),
    price          INTEGER
);

INSERT INTO npc_vendor (
                           creature_entry,
                           item_id,
                           item_count,
                           price
                       )
                       VALUES (
                           14,
                           1,
                           10,
                           1
                       );


-- Table: creatures
DROP TABLE IF EXISTS creatures;

CREATE TABLE creatures (
    guid        INTEGER      PRIMARY KEY AUTOINCREMENT
                             DEFAULT (1),
    creature_id INTEGER,
    type        VARCHAR (60),
    zone        VARCHAR (60),
    sub_zone    VARCHAR (60) 
);

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          1,
                          11,
                          'monster',
                          'Northshire Abbey',
                          'Northshire Valley'
                      );

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          2,
                          11,
                          'monster',
                          'Northshire Abbey',
                          'Northshire Valley'
                      );

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          3,
                          11,
                          'monster',
                          'Northshire Abbey',
                          'Northshire Valley'
                      );

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          4,
                          11,
                          'monster',
                          'Northshire Abbey',
                          'Northshire Valley'
                      );

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          5,
                          11,
                          'monster',
                          'Northshire Abbey',
                          'Northshire Valley'
                      );

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          6,
                          12,
                          'monster',
                          'Northshire Abbey',
                          'Northshire Vineyards'
                      );

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          7,
                          13,
                          'fnpc',
                          'Northshire Abbey',
                          'Northshire Valley'
                      );

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          8,
                          14,
                          'vendor',
                          'Northshire Abbey',
                          'Northshire Valley'
                      );

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          9,
                          12,
                          'monster',
                          'Northshire Abbey',
                          'Northshire Vineyards'
                      );

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          10,
                          12,
                          'monster',
                          'Northshire Abbey',
                          'Northshire Vineyards'
                      );

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          11,
                          12,
                          'monster',
                          'Northshire Abbey',
                          'Northshire Vineyards'
                      );

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          12,
                          8,
                          'monster',
                          'Northshire Abbey',
                          'Northshire Vineyards'
                      );

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          13,
                          8,
                          'monster',
                          'Northshire Abbey',
                          'Northshire Vineyards'
                      );

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          14,
                          15,
                          'monster',
                          'Northshire Abbey',
                          'Northshire Vineyards'
                      );

INSERT INTO creatures (
                          guid,
                          creature_id,
                          type,
                          zone,
                          sub_zone
                      )
                      VALUES (
                          15,
                          16,
                          'monster',
                          'Northshire Abbey',
                          'A Peculiar Hut'
                      );


-- Table: item_template
DROP TABLE IF EXISTS item_template;

CREATE TABLE item_template (
    entry      INTEGER      PRIMARY KEY,
    name       VARCHAR (60),
    type       VARCHAR (30),
    sub_type   VARCHAR (30),
    armor      INTEGER,
    health     INTEGER,
    mana       INTEGER,
    strength   INTEGER,
    agility    INTEGER,
    buy_price  INTEGER,
    sell_price INTEGER,
    min_dmg    INTEGER,
    max_dmg    INTEGER,
    quest_ID   INTEGER,
    effect     INTEGER
);

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              1,
                              'Wolf Meat',
                              'misc',
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              1,
                              1,
                              '',
                              '',
                              2,
                              NULL
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              2,
                              'Wolf Pelt',
                              'misc',
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              1,
                              1,
                              '',
                              NULL,
                              0,
                              NULL
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              3,
                              'Worn Axe',
                              'weapon',
                              NULL,
                              0,
                              0,
                              0,
                              0,
                              0,
                              1,
                              1,
                              2,
                              6,
                              0,
                              NULL
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              4,
                              'Strength Potion',
                              'potion',
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              1,
                              1,
                              '',
                              '',
                              0,
                              1
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              5,
                              'Wolf Steak',
                              'misc',
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              1,
                              1,
                              '',
                              '',
                              '',
                              NULL
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              9,
                              'Garrick''s Head',
                              'misc',
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              0,
                              0,
                              '',
                              '',
                              3,
                              NULL
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              10,
                              'Linen Cloth',
                              'misc',
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              1,
                              1,
                              '',
                              NULL,
                              NULL,
                              NULL
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              11,
                              'Crimson Defias Bandana',
                              'equipment',
                              'headpiece',
                              20,
                              5,
                              0,
                              1,
                              2,
                              1,
                              1,
                              NULL,
                              NULL,
                              NULL,
                              NULL
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              12,
                              'Blackened Defias Shoulderpad',
                              'equipment',
                              'shoulderpad',
                              12,
                              2,
                              0,
                              0,
                              3,
                              1,
                              1,
                              NULL,
                              NULL,
                              NULL,
                              NULL
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              13,
                              'Blackened Defias Belt',
                              'equipment',
                              'chestguard',
                              15,
                              5,
                              '',
                              2,
                              1,
                              1,
                              1,
                              NULL,
                              NULL,
                              NULL,
                              NULL
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              14,
                              'Stolen Necklace',
                              'equipment',
                              'necklace',
                              NULL,
                              1,
                              4,
                              NULL,
                              NULL,
                              1,
                              1,
                              NULL,
                              NULL,
                              NULL,
                              NULL
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              15,
                              'Blackened Defias Wristbands',
                              'equipment',
                              'bracer',
                              7,
                              1,
                              NULL,
                              1,
                              NULL,
                              1,
                              1,
                              NULL,
                              NULL,
                              NULL,
                              NULL
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              16,
                              'Blackened Defias Gloves',
                              'equipment',
                              'gloves',
                              5,
                              2,
                              NULL,
                              1,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              17,
                              'Blackened Defias Belt',
                              'equipment',
                              'belt',
                              9,
                              2,
                              NULL,
                              2,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              18,
                              'Blackened Defias Leggings',
                              'equipment',
                              'leggings',
                              18,
                              3,
                              NULL,
                              NULL,
                              4,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL
                          );

INSERT INTO item_template (
                              entry,
                              name,
                              type,
                              sub_type,
                              armor,
                              health,
                              mana,
                              strength,
                              agility,
                              buy_price,
                              sell_price,
                              min_dmg,
                              max_dmg,
                              quest_ID,
                              effect
                          )
                          VALUES (
                              19,
                              'Blackened Defias Boots',
                              'equipment',
                              'boots',
                              9,
                              2,
                              NULL,
                              NULL,
                              1,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL,
                              NULL
                          );


-- Table: loot_table
DROP TABLE IF EXISTS loot_table;

CREATE TABLE loot_table (
    entry         INTEGER PRIMARY KEY AUTOINCREMENT,
    item1_ID      INTEGER DEFAULT (0),
    item1_chance  INTEGER DEFAULT (0),
    item2_ID      INTEGER DEFAULT (0),
    item2_chance  INTEGER DEFAULT (0),
    item3_ID      INTEGER DEFAULT (0),
    item3_chance  INTEGER DEFAULT (0),
    item4_ID      INTEGER DEFAULT (0),
    item4_chance  INTEGER DEFAULT (0),
    item5_ID      INTEGER DEFAULT (0),
    item5_chance  INTEGER DEFAULT (0),
    item6_ID      INTEGER DEFAULT (0),
    item6_chance  INTEGER DEFAULT (0),
    item7_ID      INTEGER DEFAULT (0),
    item7_chance  INTEGER DEFAULT (0),
    item8_ID      INTEGER DEFAULT (0),
    item8_chance  INTEGER DEFAULT (0),
    item9_ID      INTEGER DEFAULT (0),
    item9_chance  INTEGER DEFAULT (0),
    item10_ID     INTEGER DEFAULT (0),
    item10_chance INTEGER DEFAULT (0),
    item11_ID     INTEGER DEFAULT (0),
    item11_chance INTEGER DEFAULT (0),
    item12_ID     INTEGER DEFAULT (0),
    item12_chance INTEGER DEFAULT (0),
    item13_ID     INTEGER DEFAULT (0),
    item13_chance INTEGER DEFAULT (0),
    item14_ID     INTEGER DEFAULT (0),
    item14_chance INTEGER DEFAULT (0),
    item15_ID     INTEGER DEFAULT (0),
    item15_chance INTEGER DEFAULT (0),
    item16_ID     INTEGER DEFAULT (0),
    item16_chance INTEGER DEFAULT (0),
    item17_ID     INTEGER DEFAULT (0),
    item17_chance INTEGER DEFAULT (0),
    item18_ID     INTEGER DEFAULT (0),
    item18_chance INTEGER DEFAULT (0),
    item19_ID     INTEGER DEFAULT (0),
    item19_chance INTEGER DEFAULT (0),
    item20_ID     INTEGER DEFAULT (0),
    item20_chance INTEGER DEFAULT (0) 
);

INSERT INTO loot_table (
                           entry,
                           item1_ID,
                           item1_chance,
                           item2_ID,
                           item2_chance,
                           item3_ID,
                           item3_chance,
                           item4_ID,
                           item4_chance,
                           item5_ID,
                           item5_chance,
                           item6_ID,
                           item6_chance,
                           item7_ID,
                           item7_chance,
                           item8_ID,
                           item8_chance,
                           item9_ID,
                           item9_chance,
                           item10_ID,
                           item10_chance,
                           item11_ID,
                           item11_chance,
                           item12_ID,
                           item12_chance,
                           item13_ID,
                           item13_chance,
                           item14_ID,
                           item14_chance,
                           item15_ID,
                           item15_chance,
                           item16_ID,
                           item16_chance,
                           item17_ID,
                           item17_chance,
                           item18_ID,
                           item18_chance,
                           item19_ID,
                           item19_chance,
                           item20_ID,
                           item20_chance
                       )
                       VALUES (
                           1,
                           1,
                           70,
                           2,
                           70,
                           4,
                           5,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0
                       );

INSERT INTO loot_table (
                           entry,
                           item1_ID,
                           item1_chance,
                           item2_ID,
                           item2_chance,
                           item3_ID,
                           item3_chance,
                           item4_ID,
                           item4_chance,
                           item5_ID,
                           item5_chance,
                           item6_ID,
                           item6_chance,
                           item7_ID,
                           item7_chance,
                           item8_ID,
                           item8_chance,
                           item9_ID,
                           item9_chance,
                           item10_ID,
                           item10_chance,
                           item11_ID,
                           item11_chance,
                           item12_ID,
                           item12_chance,
                           item13_ID,
                           item13_chance,
                           item14_ID,
                           item14_chance,
                           item15_ID,
                           item15_chance,
                           item16_ID,
                           item16_chance,
                           item17_ID,
                           item17_chance,
                           item18_ID,
                           item18_chance,
                           item19_ID,
                           item19_chance,
                           item20_ID,
                           item20_chance
                       )
                       VALUES (
                           2,
                           10,
                           20,
                           4,
                           10,
                           3,
                           15,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0
                       );

INSERT INTO loot_table (
                           entry,
                           item1_ID,
                           item1_chance,
                           item2_ID,
                           item2_chance,
                           item3_ID,
                           item3_chance,
                           item4_ID,
                           item4_chance,
                           item5_ID,
                           item5_chance,
                           item6_ID,
                           item6_chance,
                           item7_ID,
                           item7_chance,
                           item8_ID,
                           item8_chance,
                           item9_ID,
                           item9_chance,
                           item10_ID,
                           item10_chance,
                           item11_ID,
                           item11_chance,
                           item12_ID,
                           item12_chance,
                           item13_ID,
                           item13_chance,
                           item14_ID,
                           item14_chance,
                           item15_ID,
                           item15_chance,
                           item16_ID,
                           item16_chance,
                           item17_ID,
                           item17_chance,
                           item18_ID,
                           item18_chance,
                           item19_ID,
                           item19_chance,
                           item20_ID,
                           item20_chance
                       )
                       VALUES (
                           3,
                           10,
                           50,
                           4,
                           20,
                           3,
                           20,
                           9,
                           100,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0
                       );

INSERT INTO loot_table (
                           entry,
                           item1_ID,
                           item1_chance,
                           item2_ID,
                           item2_chance,
                           item3_ID,
                           item3_chance,
                           item4_ID,
                           item4_chance,
                           item5_ID,
                           item5_chance,
                           item6_ID,
                           item6_chance,
                           item7_ID,
                           item7_chance,
                           item8_ID,
                           item8_chance,
                           item9_ID,
                           item9_chance,
                           item10_ID,
                           item10_chance,
                           item11_ID,
                           item11_chance,
                           item12_ID,
                           item12_chance,
                           item13_ID,
                           item13_chance,
                           item14_ID,
                           item14_chance,
                           item15_ID,
                           item15_chance,
                           item16_ID,
                           item16_chance,
                           item17_ID,
                           item17_chance,
                           item18_ID,
                           item18_chance,
                           item19_ID,
                           item19_chance,
                           item20_ID,
                           item20_chance
                       )
                       VALUES (
                           4,
                           14,
                           100,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0,
                           0
                       );


-- Table: level_xp_requirement
DROP TABLE IF EXISTS level_xp_requirement;

CREATE TABLE level_xp_requirement (
    level       INTEGER PRIMARY KEY AUTOINCREMENT,
    xp_required INTEGER
);

INSERT INTO level_xp_requirement (
                                     level,
                                     xp_required
                                 )
                                 VALUES (
                                     1,
                                     400
                                 );

INSERT INTO level_xp_requirement (
                                     level,
                                     xp_required
                                 )
                                 VALUES (
                                     2,
                                     800
                                 );

INSERT INTO level_xp_requirement (
                                     level,
                                     xp_required
                                 )
                                 VALUES (
                                     3,
                                     1200
                                 );

INSERT INTO level_xp_requirement (
                                     level,
                                     xp_required
                                 )
                                 VALUES (
                                     4,
                                     1800
                                 );

INSERT INTO level_xp_requirement (
                                     level,
                                     xp_required
                                 )
                                 VALUES (
                                     5,
                                     2500
                                 );

INSERT INTO level_xp_requirement (
                                     level,
                                     xp_required
                                 )
                                 VALUES (
                                     6,
                                     3000
                                 );

INSERT INTO level_xp_requirement (
                                     level,
                                     xp_required
                                 )
                                 VALUES (
                                     7,
                                     3650
                                 );

INSERT INTO level_xp_requirement (
                                     level,
                                     xp_required
                                 )
                                 VALUES (
                                     8,
                                     4250
                                 );

INSERT INTO level_xp_requirement (
                                     level,
                                     xp_required
                                 )
                                 VALUES (
                                     9,
                                     5000
                                 );

INSERT INTO level_xp_requirement (
                                     level,
                                     xp_required
                                 )
                                 VALUES (
                                     10,
                                     6000
                                 );


-- Table: levelup_stats
DROP TABLE IF EXISTS levelup_stats;

CREATE TABLE levelup_stats (
    level    INTEGER PRIMARY KEY AUTOINCREMENT,
    health   INTEGER,
    mana     INTEGER,
    strength INTEGER,
    agility  INTEGER,
    armor    INTEGER
);

INSERT INTO levelup_stats (
                              level,
                              health,
                              mana,
                              strength,
                              agility,
                              armor
                          )
                          VALUES (
                              1,
                              10,
                              10,
                              3,
                              3,
                              75
                          );

INSERT INTO levelup_stats (
                              level,
                              health,
                              mana,
                              strength,
                              agility,
                              armor
                          )
                          VALUES (
                              2,
                              4,
                              4,
                              2,
                              1,
                              15
                          );

INSERT INTO levelup_stats (
                              level,
                              health,
                              mana,
                              strength,
                              agility,
                              armor
                          )
                          VALUES (
                              3,
                              7,
                              7,
                              4,
                              2,
                              15
                          );

INSERT INTO levelup_stats (
                              level,
                              health,
                              mana,
                              strength,
                              agility,
                              armor
                          )
                          VALUES (
                              4,
                              10,
                              10,
                              7,
                              4,
                              15
                          );

INSERT INTO levelup_stats (
                              level,
                              health,
                              mana,
                              strength,
                              agility,
                              armor
                          )
                          VALUES (
                              5,
                              12,
                              11,
                              7,
                              5,
                              15
                          );

INSERT INTO levelup_stats (
                              level,
                              health,
                              mana,
                              strength,
                              agility,
                              armor
                          )
                          VALUES (
                              6,
                              13,
                              12,
                              8,
                              5,
                              15
                          );

INSERT INTO levelup_stats (
                              level,
                              health,
                              mana,
                              strength,
                              agility,
                              armor
                          )
                          VALUES (
                              7,
                              14,
                              13,
                              8,
                              5,
                              15
                          );


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
