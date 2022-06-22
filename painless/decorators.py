from django.db import connection
from functools import reduce, wraps


def log_db_queries(func):
    """log db queries count in a func
    log execution time
    log executed queries
    """

    @wraps(func)
    def _wrapped_func(*args, **kwargs):
        res = func(*args, **kwargs)
        print("-" * 80)
        print("db queries log for %s:\n" % func.__name__)
        print("TOTAL COUNT: %s" % len(connection.queries))
        print("TOTAL TIME:  %s\n" % reduce(lambda x, y: x + float(y["time"]), connection.queries, 0.0))
        for q in connection.queries:
            print("%s:  %s\n" % (q["time"], q["sql"]))
        print("-" * 80)
        return res

    return _wrapped_func
