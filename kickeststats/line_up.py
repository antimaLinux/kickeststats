"""Soccer line-up types."""
from dataclasses import dataclass
from .player import Position


POSITION_NAMES_TO_ATTRIBUTES = {
    position.name: position.name.lower()
    for position in Position
}


@dataclass
class LineUp:
    """
    Line-up for a team.

    Beware, this class is not valid (the line-up does not sum to 11).
    """

    goalkeeper: int = 1
    defender: int = 0
    midfielder: int = 0
    forward: int = 0

    def _valid(self) -> bool:
        """Check if the line-up is valid."""
        return (
            self.goalkeeper + self.defender + self.midfielder + self.forward
        ) == 11

    def __post_init__(self) -> None:
        """
        Check validity for the line-up.
        """
        if not self._valid():
            raise RuntimeError("Invalid line-up")


@dataclass
class LU343(LineUp):
    """3-4-3 line-up."""

    defender: int = 3
    midfielder: int = 4
    forward: int = 3


@dataclass
class LU433(LineUp):
    """4-3-3 line-up."""

    defender: int = 4
    midfielder: int = 3
    forward: int = 3


@dataclass
class LU352(LineUp):
    """3-5-2 line-up."""

    defender: int = 3
    midfielder: int = 5
    forward: int = 2


@dataclass
class LU442(LineUp):
    """4-4-2 line-up."""

    defender: int = 4
    midfielder: int = 4
    forward: int = 2


@dataclass
class LU532(LineUp):
    """5-3-2 line-up."""

    defender: int = 5
    midfielder: int = 3
    forward: int = 2


@dataclass
class LU451(LineUp):
    """4-5-1 line-up."""

    defender: int = 4
    midfielder: int = 5
    forward: int = 1


@dataclass
class LU541(LineUp):
    """5-4-1 line-up."""

    defender: int = 5
    midfielder: int = 4
    forward: int = 1


LINE_UP_FACTORY = {
    "3-4-3": LU343,
    "4-3-3": LU433,
    "3-5-2": LU352,
    "4-4-2": LU442,
    "5-3-2": LU532,
    "4-5-1": LU451,
    "5-4-1": LU541,
}

SORTED_LINE_UPS = [
    "3-4-3",
    "4-3-3",
    "3-5-2",
    "4-4-2",
    "5-3-2",
    "4-5-1",
    "5-4-1",
]
