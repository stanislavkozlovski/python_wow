""" This module holds custom exceptions """


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class ItemNotInInventoryError(Error):
    """ This exception is raised whenever the item we want to remove from our inventory is not there. """
    def __init__(self, message, inventory: dict, item_name: str, *args):
        self.message = message
        self.inventory = inventory
        # value that caused the error
        self.item_name = item_name

        super(Exception, self).__init__(message, inventory, item_name, args)