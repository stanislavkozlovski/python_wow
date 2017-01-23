"""
This module holds helper functions.
i.e functions that do not serve any specific purpose but are needed in multiple places
"""


def parse_int(value) -> int:
    """
    this function is used to parse data from the DB into an integer.
    because a lot of the cells can be empty, we get None as the return type. This function makes sure we
    get 0 if the value is None or empty

    !!! IMPORTANT !!!
    This is to be added to values where we would not want to cause an exception if they were None(Null), like
    the amount of gold a character has or the amount of armor an item gives.
    On other cases, like cells pointing to certain other database IDs, a missing number there makes the row
    invalid, thus we want to create an exception.
    """
    try:
        val = int(value)
        return val
    except (TypeError, ValueError):
        return 0
