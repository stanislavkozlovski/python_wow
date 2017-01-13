from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database.main import Base


class LootTable(Base):
    """
    The loot table of a specific monster.
    entry - the unique ID of this loot table
    itemX_ID - the ID of the item this creature can drop
    itemX_chance - the chance in percentage (0-100%) for the item to drop
    entry, item1_ID, item1_chance, item2_ID, item2_chance, item3_ID, item3_chance, ... item20_ID, item20_chance
        1,       4,            55,        3,         30,          0,            0,             0,            0
    Meaning a creature whose col loot_table_ID from creature_template is equal to 1 has:
        55% chance to drop Item with ID 4
        30% chance to drop Item with ID 3
    Does not drop any more items, because the rest of the rows are 0s.
    """
    __tablename__ = 'loot_table'

    entry = Column(Integer, primary_key=True)
    item1_id = Column(Integer, ForeignKey('item_template.entry'))
    item1_chance = Column(Integer)
    item1 = relationship('ItemTemplate', foreign_keys=[item1_id])

    item2_id = Column(Integer, ForeignKey('item_template.entry'))
    item2_chance = Column(Integer)
    item2 = relationship('ItemTemplate', foreign_keys=[item2_id])

    item3_id = Column(Integer, ForeignKey('item_template.entry'))
    item3_chance = Column(Integer)
    item3 = relationship('ItemTemplate', foreign_keys=[item3_id])

    item4_id = Column(Integer, ForeignKey('item_template.entry'))
    item4_chance = Column(Integer)
    item4 = relationship('ItemTemplate', foreign_keys=[item4_id])

    item5_id = Column(Integer, ForeignKey('item_template.entry'))
    item5_chance = Column(Integer)
    item5 = relationship('ItemTemplate', foreign_keys=[item5_id])

    item6_id = Column(Integer, ForeignKey('item_template.entry'))
    item6_chance = Column(Integer)
    item6 = relationship('ItemTemplate', foreign_keys=[item6_id])

    item7_id = Column(Integer, ForeignKey('item_template.entry'))
    item7_chance = Column(Integer)
    item7 = relationship('ItemTemplate', foreign_keys=[item7_id])

    item8_id = Column(Integer, ForeignKey('item_template.entry'))
    item8_chance = Column(Integer)
    item8 = relationship('ItemTemplate', foreign_keys=[item8_id])

    item9_id = Column(Integer, ForeignKey('item_template.entry'))
    item9_chance = Column(Integer)
    item9 = relationship('ItemTemplate', foreign_keys=[item9_id])

    item10_id = Column(Integer, ForeignKey('item_template.entry'))
    item10_chance = Column(Integer)
    item10 = relationship('ItemTemplate', foreign_keys=[item10_id])

    item11_id = Column(Integer, ForeignKey('item_template.entry'))
    item11_chance = Column(Integer)
    item11 = relationship('ItemTemplate', foreign_keys=[item11_id])

    item12_id = Column(Integer, ForeignKey('item_template.entry'))
    item12_chance = Column(Integer)
    item12 = relationship('ItemTemplate', foreign_keys=[item12_id])

    item13_id = Column(Integer, ForeignKey('item_template.entry'))
    item13_chance = Column(Integer)
    item13 = relationship('ItemTemplate', foreign_keys=[item13_id])

    item14_id = Column(Integer, ForeignKey('item_template.entry'))
    item14_chance = Column(Integer)
    item14 = relationship('ItemTemplate', foreign_keys=[item14_id])

    item15_id = Column(Integer, ForeignKey('item_template.entry'))
    item15_chance = Column(Integer)
    item15 = relationship('ItemTemplate', foreign_keys=[item15_id])

    item16_id = Column(Integer, ForeignKey('item_template.entry'))
    item16_chance = Column(Integer)
    item16 = relationship('ItemTemplate', foreign_keys=[item16_id])

    item17_id = Column(Integer, ForeignKey('item_template.entry'))
    item17_chance = Column(Integer)
    item17 = relationship('ItemTemplate', foreign_keys=[item17_id])

    item18_id = Column(Integer, ForeignKey('item_template.entry'))
    item18_chance = Column(Integer)
    item18 = relationship('ItemTemplate', foreign_keys=[item18_id])

    item19_id = Column(Integer, ForeignKey('item_template.entry'))
    item19_chance = Column(Integer)
    item19 = relationship('ItemTemplate', foreign_keys=[item19_id])

    item20_id = Column(Integer, ForeignKey('item_template.entry'))
    item20_chance = Column(Integer)
    item20 = relationship('ItemTemplate', foreign_keys=[item20_id])
