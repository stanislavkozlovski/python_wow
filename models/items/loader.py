from models.items.item_template import ItemTemplate

from database.main import session


def load_item(item_id: int):
    """
    Load an item from item_template, convert it to a object of Class Item and return it
    """
    if item_id <= 0 or item_id is None:
        raise Exception("There is no such item with an ID that's 0 or negative!")

    item_template_info: ItemTemplate = session.query(ItemTemplate).get(item_id)

    return item_template_info.convert_to_item_object()
