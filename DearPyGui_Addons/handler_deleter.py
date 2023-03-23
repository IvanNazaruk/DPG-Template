from __future__ import annotations

import dearpygui.dearpygui as dpg


class HandlerDeleter:
    """
    Prevents the DPG from shutting down suddenly.
    Removes the Handler after a period of time.
    """
    deletion_queue = []

    __thread: bool = False

    @classmethod
    def add(cls, handler: int | str):
        """
        Adds a handler to the deletion queue
        :param handler: DPG handler
        """
        if not cls.__thread:
            cls.__thread = True
            # threading.Thread(target=cls._worker, daemon=True).start()
        cls.deletion_queue.append(handler)

    @classmethod
    def _worker(cls):
        while True:
            for _ in range(2):
                dpg.split_frame()

            if len(cls.deletion_queue) == 0:
                break

            deletion_queue = cls.deletion_queue.copy()
            cls.deletion_queue.clear()

            for _ in range(60):
                dpg.split_frame()

            while len(deletion_queue) > 0:
                deletion_part = deletion_queue[:25]
                del deletion_queue[:25]

                for _ in range(3):
                    dpg.split_frame()

                for handler in deletion_part:
                    try:
                        dpg.delete_item(handler)
                    except Exception:
                        pass
            del deletion_queue
        cls.__thread = False
