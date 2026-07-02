import asyncio
from typing import Callable

from flet import (
    Animation,
    AnimationCurve,
    Colors,
    Container,
    Icon,
    Icons,
    Row,
    Text,
)


class AnimatedButton(Container):
    def __init__(
        self,
        on_click: Callable[[any], None] | None = None,
        final_width: int = 155,
        text: str | None = None,
        icon: Icons | None = None
    ):
        super().__init__()
        self.final_width = final_width
        self.text = text
        self.icon = icon
        self.content = Row(
            controls=[
                Icon(self.icon, color=Colors.WHITE, visible=self.icon is not None),
                Text(self.text, color=Colors.WHITE),
            ],
            tight=True,
        )
        self.bgcolor = Colors.DEEP_PURPLE_ACCENT_200
        self.padding = 10
        self.border_radius = 20
        self.on_click = on_click
        self.ink = True
        self.width = 0
        self.animate = Animation(300, AnimationCurve.DECELERATE)
        self.running = False

    def did_mount(self):
        if not self.page:
            return

        self.page.run_task(self.__anim)
        return super().did_mount()

    async def __anim(self):
        self.width = self.final_width
        await asyncio.sleep(0.1)
        self.update()
