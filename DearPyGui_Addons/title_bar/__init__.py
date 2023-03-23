import platform

if platform.system() == "Windows":
    from .windows import *
