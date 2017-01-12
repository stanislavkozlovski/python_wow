from sqlalchemy import Column, Integer

from database.main import Base


class NpcVendor(Base):
    __tablename__ = 'npc_vendor'
    creature_entry = Column(Integer, primary_key=True)
    item_id = Column(Integer)
    item_count = Column(Integer)
    price = Column(Integer)