import debugger.pycharm

last_connectible_debugger = None


def init():
    global last_connectible_debugger

    last_connectible_debugger = first_available_debugger()


def first_available_debugger():
    for next_debugger in [pycharm]:
        if next_debugger.can_connect():
            return next_debugger

    return None


def can_connect_to_debugger():
    global last_connectible_debugger

    return last_connectible_debugger is not None


def inject_debugger():
    if can_connect_to_debugger():
        last_connectible_debugger.inject_debugger()
    else:
        raise RuntimeError('Tried connecting to debugger but none is available')

init()
