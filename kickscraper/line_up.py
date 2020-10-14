"""Soccer lineup types."""
from dataclasses import dataclass


@dataclass
class LineUp:
    """
    Line-up for a team.

    Beware, this class is not valid (the line-up does not sum to 11).
    """

    goal_keeper: int = 1
    defenders: int = 0
    midfielders: int = 0
    forwards: int = 0

    def _valid(self) -> bool:
        """Check if the lineup is valid."""
        return (
            self.goal_keeper + self.defenders +
            self.midfielders + self.forwards
        ) == 11

    def __post_init__(self) -> None:
        """
        Check validity for the line-up.
        """
        if not self._valid():
            raise RuntimeError('Invalid line-up')


@dataclass
class LU343(LineUp):
    """3-4-3 line-up."""

    defenders: int = 3
    midfielders: int = 4
    forwards: int = 3


@dataclass
class LU433(LineUp):
    """4-3-3 line-up."""

    defenders: int = 4
    midfielders: int = 3
    forwards: int = 3


@dataclass
class LU352(LineUp):
    """3-5-2 line-up."""

    defenders: int = 3
    midfielders: int = 5
    forwards: int = 2


@dataclass
class LU442(LineUp):
    """4-4-2 line-up."""

    defenders: int = 4
    midfielders: int = 4
    forwards: int = 2


@dataclass
class LU532(LineUp):
    """5-3-2 line-up."""

    defenders: int = 5
    midfielders: int = 3
    forwards: int = 2


@dataclass
class LU451(LineUp):
    """4-5-1 line-up."""

    defenders: int = 4
    midfielders: int = 5
    forwards: int = 1


@dataclass
class LU541(LineUp):
    """5-4-1 line-up."""

    defenders: int = 5
    midfielders: int = 4
    forwards: int = 1


LINE_UP_FACTORY = {
    '3-4-3': LU343,
    '4-3-3': LU433,
    '3-5-2': LU352,
    '4-4-2': LU442,
    '5-3-2': LU532,
    '4-5-1': LU451,
    '5-4-1': LU541
}
