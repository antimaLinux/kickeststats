"""Player utitlities."""
import hashlib
import pandas as pd
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Callable, Any, Dict


class Position(Enum):
    """Player position in the pitch."""

    GOALKEEPER = auto()
    DEFENDER = auto()
    MIDFIELDER = auto()
    FORWARD = auto()


# NOTE: string to set to allow multilingual support.
PLAYER_DICTIONARY_KEYS_MAPPING = {
    "name": {"Giocatore", "name"},
    "position": {"Pos", "position"},
    "value": {"CR", "value"},
    "team": {"Squadra", "team"},
    "points": {"PTS", "points"},
    "minutes": {"Minuti", "minutes"},
}

# NOTE: supporting multiple languages.
POSITION_MAPPINGS = {
    "Por": Position.GOALKEEPER,
    "Dif": Position.DEFENDER,
    "Cen": Position.MIDFIELDER,
    "Att": Position.FORWARD,
    Position.GOALKEEPER: Position.GOALKEEPER,
    Position.DEFENDER: Position.DEFENDER,
    Position.MIDFIELDER: Position.MIDFIELDER,
    Position.FORWARD: Position.FORWARD,
    "GOALKEEPER": Position.GOALKEEPER,
    "DEFENDER": Position.DEFENDER,
    "MIDFIELDER": Position.MIDFIELDER,
    "FORWARD": Position.FORWARD,
}

PLAYER_NAME_FN: Callable[[Any], str] = str.__call__
TEAM_FN: Callable[[Any], str] = str.__call__
PLAYER_POSITION_FN: Callable[[Any], Position] = POSITION_MAPPINGS.__getitem__
PLAYER_VALUE_FN: Callable[[Any], float] = float.__call__
PLAYER_POINTS_FN: Callable[[Any], float] = float.__call__
PLAYER_MINUTES_FN: Callable[[Any], float] = float.__call__
PLAYER_DICTIONARY_KEYS_FORMATTER_FN = {
    "name": PLAYER_NAME_FN,
    "position": PLAYER_POSITION_FN,
    "team": TEAM_FN,
    "value": PLAYER_VALUE_FN,
    "points": PLAYER_POINTS_FN,
    "minutes": PLAYER_MINUTES_FN,
}


@dataclass
class Player:

    name: str
    position: Position
    team: str
    captain: bool = False
    value: float = 0.0
    points: float = 0.0
    minutes: float = 0.0

    @staticmethod
    def from_dict(player_dictionary: dict) -> "Player":
        """
        Create a player from a dictionary.

        Args:
            player_dictionary (dict): a dictionary representing a player.

        Returns:
            Player: the generated player.
        """
        player_dictionary_keys = set(player_dictionary.keys())
        player_init_kwargs: Dict[str, Any] = dict()
        for argument, keys in PLAYER_DICTIONARY_KEYS_MAPPING.items():
            # NOTE: we pick one if multiples are matching
            try:
                mapped_argument = next(iter(keys & player_dictionary_keys))
                mapped_value = player_dictionary[mapped_argument]
                player_init_kwargs[argument] = PLAYER_DICTIONARY_KEYS_FORMATTER_FN[
                    argument
                ](mapped_value)
            except StopIteration:
                continue
        return Player(**player_init_kwargs)

    @staticmethod
    def from_jsonl(filepath: str) -> List["Player"]:
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

    @staticmethod
    def from_list_to_df(players: List["Player"]) -> pd.DataFrame:
        """
        List of players to a data-frame.

        Args:
            players (List[Player]): list of players.

        Returns:
            pd.DataFrame: a data-frame with players data.
        """
        players_df = pd.DataFrame(
            players,
            columns=[
                "name",
                "position",
                "team",
                "captain",
                "value",
                "points",
                "minutes",
                "position_name",
                "position_value",
                "_id",
            ],
        )
        if not players_df.empty:
            players_df["position_name"], players_df["position_value"] = zip(
                *[
                    (position.name, position.value)
                    for position in players_df["position"]
                ]
            )
            players_df["_id"] = [
                hashlib.md5(
                    f"{row['name']}{row['position_name']}{row['team']}".encode()
                ).hexdigest()
                for _, row in players_df.iterrows()
            ]
        return players_df

    @staticmethod
    def from_df_to_list(players_df: pd.DataFrame) -> List["Player"]:
        """
        Data-frame of players to list.

        Args:
            players_df (pd.DataFrame): a data-frame with players data.

        Returns:
            List[Player]: a list of players.
        """
        print(players_df["position"])
        return [
            Player.from_dict(player_row.to_dict())
            for _, player_row in players_df.iterrows()
        ]
