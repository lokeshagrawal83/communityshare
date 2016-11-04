def is_integer(s):
    try:
        f = float(s)
        if f % 1 == 0:
            return True
        else:
            return False
    except ValueError:
        return False


def is_email(s):
    if len(s) > 7:
        if re.match(
                "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",
                s,
        ) != None:
            return True
    return False


def int_or(value, default):
    try:
        return int(value)
    except:
        return default


def clamped(low, high, value):
    return min(high, max(low, value))
