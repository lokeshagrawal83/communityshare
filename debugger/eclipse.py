import os
import socket
import sys

PYDEVD_IP = '192.168.65.1'
PYDEVD_PORT = 5678


def can_connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    result = sock.connect_ex((PYDEVD_IP, PYDEVD_PORT))
    sock.close()

    return 0 == result


def inject_debugger():
    sys.path.append(os.path.join(os.path.dirname(__file__), 'pydev-custom-eclipse.egg'))
    import pydevd

    pydevd.settrace(
        host=PYDEVD_IP,
        port=PYDEVD_PORT,
        stdoutToServer=True,
        stderrToServer=True
    )
