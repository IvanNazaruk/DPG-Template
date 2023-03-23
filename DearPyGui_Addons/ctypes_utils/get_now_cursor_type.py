import ctypes


class POINT(ctypes.Structure):
    _fields_ = [('x', ctypes.c_int), ('y', ctypes.c_int)]


class CURSORINFO(ctypes.Structure):
    _fields_ = [('cbSize', ctypes.c_uint),
                ('flags', ctypes.c_uint),
                ('hCursor', ctypes.c_void_p),
                ('ptScreenPos', POINT)]


_GetCursorInfo = ctypes.windll.user32.GetCursorInfo
_GetCursorInfo.argtypes = [ctypes.POINTER(CURSORINFO)]


def GetNowCursorType() -> int:
    info = CURSORINFO()
    info.cbSize = ctypes.sizeof(info)
    _GetCursorInfo(ctypes.byref(info))
    # print(info.cbSize, info.flags, info.hCursor, info.ptScreenPos)
    return info.hCursor
