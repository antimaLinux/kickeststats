"""Testing line-up utilities."""
import pkg_resources
from ..player import (
    Player, POSITION_MAPPINGS
)


PLAYER_EXAMPLE = {
    "Giocatore": "R. Leao", "Pos": "Att", "Squadra": "MIL",
    "PTS": 0.0, "CR": "13.50"
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


def test_players_from_jsonl():
    """Testing the initialization of a list of players from a jsonl."""
    players = Player.from_jsonl(PLAYER_JSONL_FILEPATH)
    assert len(players) > 1
