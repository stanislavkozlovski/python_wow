from database.main import connection


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
