from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Type, TypeVar
    from .animator import Animator

    AnimatorType = TypeVar('AnimatorType', bound=Animator)
    all_animations: dict[int, Type[AnimatorType]]

all_animations = {}


def update():
    for animation in tuple(all_animations.values()):
        animation.update()
