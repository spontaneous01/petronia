"""
Standard Windows functions required for the system.

The required APIs are:
    * running processes
        *
    * GUI windows
        * mapping a window to a process ID
"""

import sys
import importlib

# Top-level global def
from .funcs_any_win import SHELL__CANCEL_CALLBACK_CHAIN


def __load_functions(modules):
    import platform
    import struct

    # Ensure we're on Windows
    assert 'windows' in platform.system().lower()
    void_ptr_bits = struct.calcsize('P') * 8
    winver = sys.getwindowsversion()
    environ = {
        '32-bit': void_ptr_bits == 32,
        '64-bit': void_ptr_bits == 64,
        'release': platform.release(),
        'version': platform.version(),
        'system': platform.system(),
        'version-major': winver.major,
        'version-minor': winver.minor,
        'version-build': winver.build,
        'version-platform': winver.platform,
        'version-service_pack': winver.service_pack,
    }

    ret = {}
    for name in modules:
        if isinstance(name, str):
            try:
                mod = importlib.import_module(name, __name__)
            except:
                print("Problem loading module " + name)
                raise
        else:
            mod = name
        mod.load_functions(environ, ret)
    return ret


__FUNCTIONS = __load_functions([
    "petronia.arch.funcs_x86_win",
    "petronia.arch.funcs_x64_win",

    # any_win must ALWAYS be after the bit ones.
    "petronia.arch.funcs_any_win",

    # OS-specific come after the architecture ones
    "petronia.arch.funcs_winXP",
    "petronia.arch.funcs_winVista",
    "petronia.arch.funcs_win7",
    "petronia.arch.funcs_win8",
    "petronia.arch.funcs_win10",

])

__current_module = importlib.import_module(__name__)
for __k, __v in __FUNCTIONS.items():
    setattr(__current_module, __k, __v)
