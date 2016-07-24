import os

import debugger.pycharm
import debugger.eclipse

# imported by the pydevd module to setup path-mapping in Eclipse
local_path = os.getenv('LOCAL_CODE_PATH', '/source/code/not/found')

configured_debuggers = [ eclipse, pycharm ]
last_connectable_debugger = None


def init():
    global last_connectable_debugger

    last_connectable_debugger = first_available_debugger()


def first_available_debugger():
    for next_debugger in configured_debuggers:
        if next_debugger.can_connect():
            return next_debugger

    return None


def can_connect_to_debugger():
    global last_connectable_debugger

    return last_connectable_debugger is not None


def inject_debugger():
    if can_connect_to_debugger():
        last_connectable_debugger.inject_debugger()
    else:
        raise RuntimeError('Tried connecting to debugger but none is available')

init()
