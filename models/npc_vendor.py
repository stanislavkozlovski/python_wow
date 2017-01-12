from sqlalchemy import Column, Integer

from database.main import Base

# TODO: Rename
""" TODO: Maybe split the table, it would be more efficient to hold a VendorProduct table, then 2 vendor can point to
    1 document, rather than 2 """


class NpcVendor(Base):
    """
    This table holds information regarding a single item a vendor sells

    creature_entry - the entry of the vendor in creature_template
    item_id - the ID of the item that he's supposed to sell
    item_count - the count of items he sells at once
    price - The price in gold. By default we use the Item's item.buy_price variable in it's class.
        However, if this is set to something we override the price.
    Example:
        creature_entry, item_id, item_count, price
                13,       1,          5,    10
    The NPC whose entry is 13, sells the item with ID 1, 5 at a time for 10 gold.
    He sells the whole 5 items for 10 gold. He cannot sell 1,2,3 or 4 items, only 5 at once.
    """
    __tablename__ = 'npc_vendor'
    creature_entry = Column(Integer, primary_key=True)
    item_id = Column(Integer)
    item_count = Column(Integer)
    price = Column(Integer)