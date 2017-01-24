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


class NoSuchCharacterError(Error):
    """ This exception is raised whenever we want to load a character that is not saved in the database. """
    def __init(self, message, name: str, *args):
        self.char_name = name

        super(Exception, self).__init__(message, name, args)


class InvalidBuffError(Error):
    """ This exception is raised whenever we're trying to load a buff that is not of an approved type """
    def __init(self, message, name: str, *args):
        self.buff_name = name

        super(Exception, self).__init__(message, name, args)


class NonExistantBuffError(Error):
    """
    This exception is raised whenever we're trying to access a Buff that is not part of the object
    ex: Trying to remove a buff from a Character when he does not have it in the first place
    """

    def __init(self, message, name: str, *args):
        self.buff_name = name

        super(Exception, self).__init__(message, name, args)