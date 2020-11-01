"""Testing team utilities."""
import pytest
import pkg_resources
import pandas as pd
from loguru import logger
from kickeststats.player import Player, Position
from kickeststats.team import Team, points_to_goals, GOAL_THRESHOLD, GOAL_GAP
from kickeststats.exceptions import InvalidTeamLineup, UnsupportedLineUp


PLAYER_JSONL_FILEPATH = pkg_resources.resource_filename(
    "kickeststats", "resources/tests/players.jsonl"
)
PLAYERS = Player.from_jsonl(PLAYER_JSONL_FILEPATH)
PLAYERS_DF = Player.from_list_to_df(PLAYERS)
TEST_CASE_JSONL_FILEPATH = pkg_resources.resource_filename(
    "kickeststats", "resources/tests/players_test_case.jsonl"
)
PLAYERS_TEST_CASE = Player.from_jsonl(TEST_CASE_JSONL_FILEPATH)
PLAYERS_TEST_CASE_DF = Player.from_list_to_df(PLAYERS_TEST_CASE)
LINE_UP = "4-4-2"
TEAM_PLAYERS = [
    Player(name="L. Skorupski", position=Position.GOALKEEPER, team="BOL", captain=False, value=7.6, points=5.0),
    Player(name="Bremer", position=Position.DEFENDER, team="TOR", captain=False, value=11.9, points=32.1),
    Player(name="G. Di Lorenzo", position=Position.DEFENDER, team="NAP", captain=False, value=15.6, points=0.0),
    Player(name="J. Mojica", position=Position.DEFENDER, team="ATA", captain=False, value=9.4, points=22.3),
    Player(name="L. Tonelli", position=Position.DEFENDER, team='SAM', captain=False, value=6.3, points=0.0),
    Player(name="G. Castrovilli", position=Position.MIDFIELDER, team="FIO", captain=True, value=14.8, points=0.0),
    Player(name="M. Rog", position=Position.MIDFIELDER, team="CAG", captain=False, value=12.0, points=16.1),
    Player(name="M. Thorsby", position=Position.MIDFIELDER, team="SAM", captain=False, value=10.2, points=0.0),
    Player(name="J. Schouten", position=Position.MIDFIELDER, team="BOL", captain=False, value=8.2, points=16.8),
    Player(name="Joao Pedro", position=Position.FORWARD, team="CAG", captain=False, value=17.1, points=28.3),
    Player(name="J. Correa", position=Position.FORWARD, team="LAZ", captain=False, value=14.3, points=7.7)
]
TEAM_SUBSTITUTES = [
    Player(name="R. Marin", position=Position.MIDFIELDER, team="CAG", captain=False, value=11.7, points=12.0),
    Player(name="A. Vidal", position=Position.MIDFIELDER, team="INT", captain=False, value=15.9, points=10.8),
    Player(name="R. Vieira", position=Position.MIDFIELDER, team="VER", captain=False, value=8.2, points=0.0),
    Player(name="M. Lazzari", position=Position.MIDFIELDER, team="LAZ", captain=False, value=12.2, points=0.0),
    Player(name="F. Caputo", position=Position.FORWARD, team="SAS", captain=False, value=18.6, points=0.0),
    Player(name="Y. Karamoh", position=Position.FORWARD, team="PAR", captain=False, value=6.4, points=0.0),
    Player(name="N. Sansone", position=Position.FORWARD, team="BOL", captain=False, value=10.4, points=0.0),
    Player(name="R. Lukaku", position=Position.FORWARD, team="INT", captain=False, value=22.6, points=0.0),
    Player(name="Mario Rui", position=Position.DEFENDER, team="NAP", captain=False, value=13.2, points=0.0),
    Player(name="C. Dell'Orco", position=Position.DEFENDER, team="SPE", captain=False, value=6.4, points=4.2),
    Player(name="Rogerio", position=Position.DEFENDER, team="SAS", captain=False, value=10.4, points=0.0),
    Player(name="Marlon", position=Position.DEFENDER, team="SAS", captain=False, value=10.3, points=0.0),
    Player(name="A. Consigli", position=Position.GOALKEEPER, team="SAS", captain=False, value=10.0, points=0.0),
    Player(name="S. Scuffet", position=Position.GOALKEEPER, team="UDI", captain=False, value=6.5, points=0.0)
]


def _get_team(line_up):
    """Get team given a line-up."""
    defenders, midfielders, forwarders = map(int, line_up.split("-"))
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
            PLAYERS_DF[PLAYERS_DF["position_name"] == "GOALKEEPER"].sample(1),
            PLAYERS_DF[PLAYERS_DF["position_name"] == "DEFENDER"].sample(defenders),
            PLAYERS_DF[PLAYERS_DF["position_name"] == "MIDFIELDER"].sample(midfielders),
            PLAYERS_DF[PLAYERS_DF["position_name"] == "FORWARD"].sample(forwarders)
        ], axis=0).iterrows()
    ]


def test_team_initialization():
    """Testing the initialization of a team."""
    with pytest.raises(InvalidTeamLineup):
        _ = Team(players=PLAYERS, substitutes=PLAYERS, line_up="3-4-3")
    with pytest.raises(UnsupportedLineUp):
        _ = Team(players=_get_team("3-3-4"), substitutes=_get_team("2-2-2"), line_up="3-3-4")
    _ = Team(players=_get_team("4-3-3"), substitutes=_get_team("2-2-2"), line_up="4-3-3")


def test_team_points():
    """Testing the points calculation of a team."""
    team = Team(players=_get_team("4-4-2"), substitutes=_get_team("2-2-2"), line_up="4-4-2")
    assert team.points(PLAYERS) == 0.0
    assert team.points(PLAYERS, is_away=False) == 6.0
    # a realistic test case
    team = Team(players=TEAM_PLAYERS, substitutes=TEAM_SUBSTITUTES, line_up="4-4-2")
    assert team.points(PLAYERS_TEST_CASE) == 167.3
    assert team.points(PLAYERS_TEST_CASE, is_away=False) == 173.3


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
