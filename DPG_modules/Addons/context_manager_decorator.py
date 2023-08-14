from typing import Any


class context_manager_decorator:
    def __init__(self, context_cls: Any):
        self.context_cls = context_cls

    def __call__(self, func: Any) -> Any:
        def wrapper(*args, **kwargs):
            with self.context_cls:
                return func(*args, **kwargs)

        return wrapper
