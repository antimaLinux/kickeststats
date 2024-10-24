"""Testing player utilities."""
from typing import Any, Dict

import pkg_resources

from ..player import POSITION_MAPPINGS, Player

PLAYER_EXAMPLE: Dict[str, Any] = {
    "Giocatore": "R. Leao",
    "Pos": "Att",
    "Squadra": "MIL",
    "PTS": 0.0,
    "CR": 13.50,
}
PLAYER_JSONL_FILEPATH = pkg_resources.resource_filename(
    "kickeststats", "resources/tests/players.jsonl"
)


def test_player_from_dict():
    """Testing the initialization of a player from a dictionary."""
    player = Player.from_dict(PLAYER_EXAMPLE)
    assert player.name == PLAYER_EXAMPLE["Giocatore"]
    assert player.position == POSITION_MAPPINGS[PLAYER_EXAMPLE["Pos"]]
    assert player.value == PLAYER_EXAMPLE["CR"]
    assert player.points == PLAYER_EXAMPLE["PTS"]
    assert player.team == PLAYER_EXAMPLE["Squadra"]


def test_players_from_jsonl():
    """Testing the initialization of a list of players from a jsonl."""
    players = Player.from_jsonl(PLAYER_JSONL_FILEPATH)
    assert len(players) > 1


def test_players_from_list_to_df():
    """Testing the transformation from list of players to data-frame."""
    players = Player.from_jsonl(PLAYER_JSONL_FILEPATH)
    assert Player.from_list_to_df(players).shape[0] == len(players)
