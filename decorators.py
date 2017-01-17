from database.main import connection


def cast_spell(func):
    """
    Wraps a function that is tied to a spell cast.
    What is general for all spells is they require some resource (currently - mana)
    and have a cooldown.
    This decorator checks if both those needs are met, and if not, does not cast the spell.
    """
    def decorator(*args, **kwargs):
        self = args[0]

        if len(args) < 2:
            if len(kwargs) < 2:
                raise Exception('The cast_spell decorator function must take two arguments! self and spell!')
            spell = kwargs['spell']
        else:
            spell = args[1]
        mana_cost = spell.mana_cost
        if not self.has_enough_mana(mana_cost):
            print(f'Not enough mana! {spell.name} requires {mana_cost} but you have {self.mana}!')
            return False

        # proceed with casting the spell and start its cooldown timer
        is_ready = spell.cast()
        if not is_ready:
            print(f'{spell.name} is still on cooldown!')
            return False

        return func(*args, **kwargs)
    return decorator


def db_connection(func):
    """
    Wraps a function that connects to the database and uses a context manager
    in order to automatically commit or rollback transactions.
    """
    def decorator(*args, **kwargs):
        with connection:
            return func(*args, **kwargs)

    return decorator


def run_once(func):
    """A decorator that runs a function only once."""

    def decorated(*args, **kwargs):
        try:
            return decorated.saved_result
        except AttributeError:
            decorated.saved_result = func(*args, **kwargs)
            return decorated.saved_result

    return decorated
