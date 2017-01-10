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
