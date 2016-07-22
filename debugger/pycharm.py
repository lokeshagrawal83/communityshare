import os
import socket
import sys

PYDEVD_IP = '192.168.65.1'
PYDEVD_PORT = 5001


def can_connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((PYDEVD_IP, PYDEVD_PORT))
    sock.close()

    return 0 == result


def inject_debugger():
    sys.path.append(os.path.join(os.path.dirname(__file__), 'pycharm-debug-py3k.egg'))
    import pydevd

    pydevd.settrace(
        PYDEVD_IP,
        port=PYDEVD_PORT,
        stdoutToServer=True,
        stderrToServer=True
    )
