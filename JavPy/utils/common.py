import datetime
import functools
import re

version = "0.3.8"


def try_evaluate(lambda_expression, default=None):
    def evaluate(expression):
        try:
            return expression(), None
        except Exception as ex:
            return default, ex

    return evaluate(lambda_expression)


def cache(func):
    __cache = dict()

    @functools.wraps(func)
    def _wrapped(*args, **kwargs):
        key = str(args) + "///" + str(kwargs)

        if key in __cache:
            if datetime.datetime.now() - __cache[key][0] < datetime.timedelta(hours=1):
                return __cache[key][1]

        res = func(*args, **kwargs)

        if res:
            __cache[key] = (datetime.datetime.now(), res)

        return res

    return _wrapped


_class_name_pattern = re.compile(r"\.(.+?)\s")


def get_func_full_name(func):
    try:
        return func.__module__ + "." + func.__qualname__
    except AttributeError:
        try:
            return (
                func.__module__
                + re.search(_class_name_pattern, func.im_class).group(1)
                + "."
                + func.__name__
            )
        except AttributeError:
            return ""


def assign(origin, new):
    for k in new.__dict__.keys():
        v = getattr(new, k)
        if v:
            setattr(origin, k, v)
    return origin


def conclude(objects):
    if objects is None:
        return None
    objects = list(filter(lambda x: x, objects))
    if len(objects) == 0:
        return None
    if len(objects) == 1:
        return objects[0]
    return functools.reduce(assign, objects)


def urlencode(string, encoding):
    from urllib.parse import quote
    return quote(string.encode(encoding))


def urldecode(string, encoding):
    from urllib.parse import unquote
    return unquote(string, encoding)


def get_code_from_title(title):
    return re.search(r"\w+-?\d+", title).group(0)
