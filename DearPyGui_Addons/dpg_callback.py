from __future__ import annotations

import threading
import traceback
from typing import Callable, Sequence


class dpg_callback:
    BLOCKER = False
    function_queue: list[Callable, Sequence] | None = None

    def __init__(self, sender: bool = False, app_data: bool = False, user_data: bool = False):
        self.sender = sender
        self.app_data = app_data
        self.user_data = user_data

    def __call__(self, function=None):
        def wrapper(cls, sender_var=None, app_data_var=None, user_data_var=None):
            bool_list = [True, self.sender, self.app_data, self.user_data]
            args = [cls, sender_var, app_data_var, user_data_var]
            # remove cls if is not object (self)
            if isinstance(args[0], (int, float, str)):
                del args[-1]  # arguments shifted to the left
                del bool_list[0]
            # remove unnecessary arguments
            args = [item for item, include in zip(args, bool_list) if include]

            if self.BLOCKER:
                self.function_queue = [function, args]
                return
            self.BLOCKER = True

            def run(_function: Callable, _args: Sequence):
                while True:
                    try:
                        _function(*_args)
                    except Exception:
                        traceback.print_exc()
                    if self.function_queue is None:
                        self.BLOCKER = False
                        return

                    _function, _args = self.function_queue
                    self.function_queue = None

            threading.Thread(target=run, args=(function, args,), daemon=True).start()

        return wrapper
