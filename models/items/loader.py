from models.items.item_template import ItemTemplateSchema

from database.main import session


def load_item(item_id: int):
    """
    Load an item from item_template, convert it to a object of Class Item and return it
    """
    if item_id <= 0 or not isinstance(item_id, int):
        raise Exception("There is no such item with an ID that's 0 or negative!")

    item_template_info: ItemTemplateSchema = session.query(ItemTemplateSchema).get(item_id)

    if item_template_info is None:
        raise Exception(f'There is no such item with an ID {item_id}!')

    return item_template_info.convert_to_item_object()
