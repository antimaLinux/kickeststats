"""Player utitlities."""
from typing import List
from enum import Enum, auto
from dataclasses import dataclass


class Position(Enum):
    """Player position in the pitch."""

    GOALKEEPER = auto()
    DEFENDER = auto()
    MIDFIELDER = auto()
    FORWARD = auto()


# NOTE: string to set to allow multilingual support.
PLAYER_DICTIONARY_KEYS_MAPPING = {
    'name': {'Giocatore'},
    'position': {'Pos'},
    'value': {'CR'}
}

# NOTE: supporting multiple languages.
POSITION_MAPPINGS = {
    'Por': Position.GOALKEEPER,
    'Dif': Position.DEFENDER,
    'Cen': Position.MIDFIELDER,
    'Att': Position.FORWARD
}

PLAYER_DICTIONARY_KEYS_FORMATTER_FN = {
    'name': str,
    'position': POSITION_MAPPINGS.__getitem__,
    'value': float
}


@dataclass
class Player:

    name: str
    position: Position
    value: float

    @staticmethod
    def from_dict(player_dictionary: dict) -> 'Player':
        """
        Create a player from a dictionary.

        Args:
            player_dictionary (dict): a dictionary representing a player.

        Returns:
            Player: the generated player.
        """
        player_dictionary_keys = set(player_dictionary.keys())
        player_init_kwargs = dict()
        for argument, keys in PLAYER_DICTIONARY_KEYS_MAPPING.items():
            # NOTE: we pick one if multiples are matching
            mapped_argument = next(iter(keys & player_dictionary_keys))
            mapped_value = player_dictionary[mapped_argument]
            player_init_kwargs[argument] = (
                PLAYER_DICTIONARY_KEYS_FORMATTER_FN[argument](mapped_value)
            )
        return Player(**player_init_kwargs)

    @staticmethod
    def from_jsonl(filepath: str) -> List['Player']:
        """
        Parse players from JSONL.

        Args:
            filepath (str): path to the JSONL file containing players
                information.

        Returns:
            List[Player]: list of players.
        """
        with open(filepath) as fp:
            players = [
                # NOTE: using eval to handle single quotes
                Player.from_dict(eval(line.strip()))
                for line in fp
            ]
        return players
