"""Team utilities."""
import pandas as pd
from typing import List
from .player import Player
from .exceptions import UnsupportedLineUp, InvalidTeamLineup
from .line_up import LINE_UP_FACTORY, POSITION_NAMES_TO_ATTRIBUTES

MAX_SUBSTITUTIONS = 5


class Team:
    """Team definition."""

    def __init__(
        self, players: List[Player], line_up: str, substitutes: List[Player] = []
    ):
        """
        Initialize the team.

        Args:
            players (List[Player]): players in the starting line-up.
            line_up (str): type of line-up.
                Currently supported:
                - "3-4-3"
                - "4-3-3"
                - "3-5-2"
                - "4-4-2"
                - "5-3-2"
                - "4-5-1"
                - "5-4-1"
            substitutes (List[Player], optional): players on the bench. Defaults to [],
                a.k.a., no substitutes.

        Raises:
            UnsupportedLineUp: the line-up requested is not supported.
        """
        self.players = Player.from_list_to_df(players)
        self.substitutes = Player.from_list_to_df(substitutes)
        if line_up not in LINE_UP_FACTORY:
            raise UnsupportedLineUp(line_up)
        else:
            self.line_up = LINE_UP_FACTORY[line_up]
        # validate list of players against the line-ip
        for position_name, count in self.players.groupby(
            "position_name"
        ).size().to_dict().items():
            if getattr(self.line_up, POSITION_NAMES_TO_ATTRIBUTES[position_name]) != count:
                raise InvalidTeamLineup(
                    f"{count} {POSITION_NAMES_TO_ATTRIBUTES[position_name]}(s) "
                    f"not compatible with {line_up}"
                )

    def points(self, players: List[Player], is_away: bool = True) -> float:
        """
        Evaluate the team.

        Args:
            players (List[Player]): players with statistics.
            is_away (bool, optional): is the team away. Defaults to False.

        Returns:
            float: points for the team.
        """
        all_players = Player.from_list_to_df(players)
        all_players_with_points = all_players["points"] > 0.0
        # candidate players
        playing_players = all_players[
            all_players["_id"].isin(self.players["_id"])
        ]
        # substitutes
        substitutes = all_players[
            all_players_with_points & all_players["_id"].isin(self.substitutes["_id"])
        ].sort_values(by="points", ascending=False)
        if not substitutes.empty:
            # replace the worst candidate players one by one
            candidates_for_substitution = playing_players[playing_players["points"] == 0.0]
            to_be_substituted_ids: List[str] = []
            substitutes_ids: List[str] = []
            for _, player in candidates_for_substitution.iterrows():
                substitutes_per_position = substitutes[
                    substitutes["position_name"] == player["position_name"] & ~substitutes["_id"].isin(substitutes_ids)
                ]
                if not substitutes_per_position.empty:
                    to_be_substituted_ids.append(player["_id"])
                    # NOTE: sorted descending per points
                    substitutes_ids.append(substitutes.iloc[0]["_id"])
                if len(to_be_substituted_ids) == MAX_SUBSTITUTIONS:
                    break
            # get the final list
            playing_players = pd.concat([
                playing_players[~playing_players["_id"].isin(to_be_substituted_ids)],
                substitutes[substitutes["_id"].isin(substitutes_ids)]
            ], axis=0)
        # compute the points
        points = 0.0 if is_away else 6.0
        for _, player in playing_players.iterrows():
            points += (
                2 * player["points"] if player["captain"] else player["points"]
            )
        return points
