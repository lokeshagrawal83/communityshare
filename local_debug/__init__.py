import local_debug.pycharm


def first_available_debugger():
    for debugger in [pycharm]:
        if debugger.can_connect():
            return debugger

    return None

last_connectible_debugger = first_available_debugger()


def can_connect_to_debugger():
    global last_connectible_debugger

    return last_connectible_debugger is not None


def inject_debugger():
    if can_connect_to_debugger():
        last_connectible_debugger.inject_debugger()
    else:
        raise RuntimeError('Tried connecting to debugger but none is available')
