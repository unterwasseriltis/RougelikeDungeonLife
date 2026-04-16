from .base import Component
from .position import Position
from .renderable import Renderable
from .actor import Actor
from .fighter import Fighter
from .death import Death        # ← neu

__all__ = ["Component", "Position", "Renderable", "Actor", "Fighter", "Death"]