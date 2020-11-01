"""Testing team utilities."""
import pytest
import pkg_resources
import pandas as pd
from loguru import logger
from ..player import Player
from ..team import Team, points_to_goals, GOAL_THRESHOLD, GOAL_GAP
from ..exceptions import InvalidTeamLineup, UnsupportedLineUp


PLAYER_JSONL_FILEPATH = pkg_resources.resource_filename(
    "kickeststats", "resources/tests/players.jsonl"
)
PLAYERS = Player.from_jsonl(PLAYER_JSONL_FILEPATH)
PLAYERS_DF = Player.from_list_to_df(PLAYERS)


def _get_team(line_up):
    """Get team given a line-up."""
    defenders, midfielders, forwarders = map(int, line_up.split('-'))
    return [
        Player(
            name=player["name"],
            position=player["position"],
            team=player["team"],
            captain=player["captain"],
            value=player["value"],
            points=player["points"]
        )
        for _, player in pd.concat([
            PLAYERS_DF[PLAYERS_DF['position_name'] == 'GOALKEEPER'].sample(1),
            PLAYERS_DF[PLAYERS_DF['position_name'] == 'DEFENDER'].sample(defenders),
            PLAYERS_DF[PLAYERS_DF['position_name'] == 'MIDFIELDER'].sample(midfielders),
            PLAYERS_DF[PLAYERS_DF['position_name'] == 'FORWARD'].sample(forwarders)
        ], axis=0).iterrows()
    ]


def test_team_initialization():
    """Testing the initialization of a team."""
    with pytest.raises(InvalidTeamLineup):
        _ = Team(players=PLAYERS, substitutes=PLAYERS, line_up='3-4-3')
    with pytest.raises(UnsupportedLineUp):
        _ = Team(players=_get_team('3-3-4'), substitutes=_get_team('2-2-2'), line_up='3-3-4')
    _ = Team(players=_get_team('4-3-3'), substitutes=_get_team('2-2-2'), line_up='4-3-3')


def test_team_points():
    """Testing the points calculation of a team."""
    team = Team(players=_get_team('4-4-2'), substitutes=_get_team('2-2-2'), line_up='4-4-2')
    assert team.points(PLAYERS) == 0.0
    assert team.points(PLAYERS, is_away=False) == 6.0


def test_points_to_goals():
    """Testing the conversion from points to goals."""
    points = GOAL_THRESHOLD - GOAL_GAP // 2
    goals = 0
    while points < 400.:
        converted_goals = points_to_goals(points)
        logger.info(f"{points} points converted to {converted_goals}")
        assert goals == converted_goals
        goals += 1
        points += GOAL_GAP
