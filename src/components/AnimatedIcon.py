import asyncio
from abc import ABC, abstractmethod

from flet import (
    Animation,
    AnimationCurve,
    Colors,
    ColorValue,
    Icon,
    Icons,
    IconValue,
    Rotate,
    alignment,
)


class AnimatedIcon(ABC, Icon):
    def __init__(
        self,
        icon: IconValue | None = None,
        color: ColorValue | None = None,
        size: int = 30,
    ):
        super().__init__()
        self.name = icon
        self.color = color
        self.size = size
        self.animate_opacity = Animation(300, AnimationCurve.DECELERATE)
        self.animate_rotation = Animation(300, AnimationCurve.DECELERATE)
        self.animate_offset = Animation(300, AnimationCurve.DECELERATE)
        self.animate_scale = Animation(300, AnimationCurve.DECELERATE)
        self.animate_size = Animation(300, AnimationCurve.DECELERATE)
        self.running = False

    def did_mount(self):
        self.running = True
        self.page.run_task(self._anim)
        return super().did_mount()

    def will_unmount(self):
        self.running = False
        return super().will_unmount()

    @abstractmethod
    async def _anim(self):
        pass


class RotatingSettingsWheel(AnimatedIcon):
    def __init__(self, size: int = 30):
        super().__init__(Icons.SETTINGS, Colors.DEEP_PURPLE_ACCENT_200, size)
        self.rotate = Rotate(0, alignment=alignment.center)

    async def _anim(self):
        while self.running:
            self.rotate.angle += 0.2
            self.update()
            await asyncio.sleep(0.1)
