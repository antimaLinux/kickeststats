"""Team utilities."""
import os
from collections import Counter
from random import random
from typing import List

import numpy as np
import pandas as pd
from loguru import logger

from .exceptions import InvalidTeamLineup, UnsupportedLineUp
from .line_up import (
    LINE_UP_FACTORY,
    POSITION_MAXIMUM,
    POSITION_MINIMUM,
    POSITION_NAMES_TO_ATTRIBUTES,
    SORTED_LINE_UPS,
)
from .player import Player

MAX_SUBSTITUTIONS = int(os.environ.get("KICKESTSTATS_MAX_SUBSTITUTIONS", 5))
GOAL_THRESHOLD = float(os.environ.get("KICKESTSTATS_GOAL_THRESHOLD", 180))
GOAL_GAP = float(os.environ.get("KICKESTSTATS_GOAL_GAP", 20))
MINUTES_THRESHOLD = float(os.environ.get("KICKESTSTATS_MINUTES_THRESHOLD", 15))
POINTS_THRESHOLD = float(os.environ.get("KICKESTSTATS_POINTS_THRESHOLD", 15))
HOME_BONUS = float(os.environ.get("KICKESTSTATS_HOME_BONUS", 6))
CAPTAIN_MODIFIER = float(os.environ.get("KICKESTSTATS_CAPTAIN_MODIFIER", 1.5))


def points_to_goals(points: float) -> int:
    """
    Convert points to goals.

    Args:
        points (float): points.

    Returns:
        int: [description]
    """
    goals = 0
    threshold = GOAL_THRESHOLD
    while points >= threshold:
        goals += 1
        threshold += GOAL_GAP
    return goals


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
        self.line_up = line_up
        self._validate_line_up(self.players, line_up)

    def _validate_line_up(self, players: pd.DataFrame, line_up: str):
        """Validate a player list against a line-up.

        Args:
            players: players to consider.
            line_up: line-up type.

        Raises:
            UnsupportedLineUp: the line-up requested is not supported.
        """
        if line_up not in LINE_UP_FACTORY:
            raise UnsupportedLineUp(line_up)
        else:
            line_up_object = LINE_UP_FACTORY[line_up]
        for position_name, count in (
            players.groupby("position_name").size().to_dict().items()
        ):
            if (
                getattr(line_up_object, POSITION_NAMES_TO_ATTRIBUTES[position_name])
                != count
            ):
                logger.debug(
                    f"{count} {POSITION_NAMES_TO_ATTRIBUTES[position_name]}(s) "
                    f"not compatible with {line_up_object}, substitutions will take place."
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
        all_players_with_valid_points = (all_players["points"] >= POINTS_THRESHOLD) | (
            all_players["minutes"] >= MINUTES_THRESHOLD
        )
        # candidate players
        playing_players = all_players[
            all_players["_id"].isin(self.players["_id"])
        ].copy()
        if self.players["captain"].any():
            captain_id = self.players[self.players["captain"]].iloc[0]["_id"]
        else:
            logger.warning("Captain not provided picking a random one")
            captain_id = self.players.sample(1, random_state=42).iloc[0]["_id"]
        playing_players.loc[:, "captain"] = playing_players["_id"] == captain_id
        logger.debug(f"Playing players: {playing_players}")
        # substitutes (preserve bench order)
        substitutes = all_players[
            all_players_with_valid_points
            & all_players["_id"].isin(self.substitutes["_id"])
        ]
        logger.debug(f"Potential substitutes: {substitutes}")
        # sort substitutes by order on the bench
        substitutes.index = substitutes["_id"]
        substitutes = substitutes.reindex(self.substitutes["_id"]).dropna()
        logger.debug(f"Reordered substitutes: {substitutes}")
        ordered_substitutes_ids_from_bench = substitutes["_id"].tolist()
        if not substitutes.empty:
            # get and sort for ascending points the candidates (we keep captain first to make sure that if needed, it's substituted)
            candidates_for_substitution = playing_players[
                (
                    (playing_players["points"] < POINTS_THRESHOLD)
                    & (playing_players["minutes"] < MINUTES_THRESHOLD)
                )
            ].sort_values(by=["captain", "points"], ascending=[False, True])[
                :MAX_SUBSTITUTIONS
            ]
            captain_to_be_substituted = captain_id in set(
                candidates_for_substitution["_id"].tolist()
            )
            logger.debug(f"Candidates for substitution: {candidates_for_substitution}")
            # NOTE: handling the goalkeeper
            remove_goalkeeper_from_substitutes = "GOALKEEPER" not in set(
                candidates_for_substitution["position_name"]
            )
            if remove_goalkeeper_from_substitutes:
                logger.debug("Optionally removing goalkeeper from substitutes")
                substitutes = substitutes[
                    ~(substitutes["position_name"] == "GOALKEEPER")
                ]
            else:
                # we make sure that the goalkeeper gets replaced first in case of need
                substitutes = pd.concat(
                    [
                        substitutes[substitutes["position_name"] == "GOALKEEPER"][:1],
                        substitutes[~(substitutes["position_name"] == "GOALKEEPER")],
                    ]
                )
                logger.debug(
                    f"Making sure goalkeeper is substituted first: {substitutes}"
                )
            # NOTE: handling position limits
            players_not_substituted = playing_players[
                ~playing_players["_id"].isin(candidates_for_substitution["_id"])
            ]
            position_counts = Counter(players_not_substituted["position_name"])
            # NOTE: sort them following the bench
            ordered_position_names = [
                position_name
                for position_name in dict.fromkeys(
                    substitutes["position_name"].tolist()
                )
                if position_name in {"DEFENDER", "MIDFIELDER", "FORWARD"}
            ]
            for position_name in ordered_position_names:
                position_maximum_delta = (
                    POSITION_MAXIMUM[position_name] - position_counts[position_name]
                )
                position_minimum_delta = (
                    POSITION_MINIMUM[position_name] - position_counts[position_name]
                )
                if position_maximum_delta <= 0:
                    logger.debug(
                        f"Reached limit for postion: {position_name}, adjusting substitutes"
                    )
                    substitutes = substitutes[
                        ~(substitutes["position_name"] == position_name)
                    ]
                else:
                    if position_minimum_delta > 0:
                        logger.debug(
                            f"Giving priority to at least {position_minimum_delta} "
                            f"substitutes for position: {position_name}"
                        )
                        priority_slicing = substitutes["_id"].isin(
                            substitutes[substitutes["position_name"] == position_name][
                                :position_minimum_delta
                            ]["_id"]
                        )
                        substitutes = pd.concat(
                            [
                                substitutes[priority_slicing],
                                substitutes[~priority_slicing],
                            ]
                        )
                    logger.debug(
                        f"Keeping at most {position_maximum_delta} substitutes for position: {position_name}"
                    )
                    current_position = substitutes["position_name"] == position_name
                    other_positions = ~current_position
                    substitutes = substitutes[
                        substitutes["_id"].isin(
                            substitutes[current_position][:position_maximum_delta][
                                "_id"
                            ]
                        )
                        | other_positions
                    ]
                logger.debug(
                    f"Substitute list after processing {position_name}: {substitutes}"
                )
            # NOTE: this could be enabled to help boost points
            # substitutes = substitutes.sort_values(by="points", ascending=False)
            # NOTE: final list of substitutes
            substitutes = substitutes[: candidates_for_substitution.shape[0]]
            # NOTE: now we make sure we follow the order of the bench respecting min-max priorities per position
            sorter = dict(
                zip(
                    ordered_substitutes_ids_from_bench,
                    range(len(ordered_substitutes_ids_from_bench)),
                )
            )
            substitutes["sorter"] = substitutes["_id"].map(sorter)
            substitutes = substitutes.sort_values(by="sorter")
            substitutes.drop("sorter", axis=1)
            logger.debug(f"Potential replacements: {substitutes}")
            to_be_substituted_ids: List[str] = candidates_for_substitution[
                "_id"
            ].tolist()
            substitutes_ids: List[str] = substitutes["_id"].tolist()
            captain_substitute_id: str = ""
            # try to find a match between the line-ups and the substitutes configuration
            line_up_found: bool = False
            for index in range(len(substitutes_ids)):
                if line_up_found:
                    break
                merge_index = len(substitutes_ids) - index
                candidate_to_be_substituted_ids = to_be_substituted_ids[:merge_index]
                candidate_substitutes_ids = substitutes_ids[:merge_index]
                # handling captain
                candidate_captain_substitute_id = ""
                try:
                    captain_row = playing_players[
                        playing_players["_id"] == captain_id
                    ].iloc[0]
                    captain_substitutes_with_same_position = substitutes[
                        substitutes["_id"].isin(candidate_substitutes_ids)
                        & (substitutes["position_name"] == captain_row["position_name"])
                    ]
                    if not captain_substitutes_with_same_position.empty:
                        candidate_captain_substitute_id = (
                            captain_substitutes_with_same_position.iloc[0]["_id"]
                        )
                    else:
                        logger.debug(
                            "Could not replace the captain by position, picking the first substitute as captain"
                        )
                        candidate_captain_substitute_id = candidate_substitutes_ids[0]
                except ValueError:
                    logger.debug("Substitution is not about the captain")
                candidate_playing_players = pd.concat(
                    [
                        playing_players[
                            ~playing_players["_id"].isin(
                                candidate_to_be_substituted_ids
                            )
                        ],
                        substitutes[substitutes["_id"].isin(candidate_substitutes_ids)],
                    ],
                    axis=0,
                )
                logger.debug(
                    f"Candidate line-up with {merge_index} substitution/s: {candidate_playing_players}"
                )
                # probing line-ups from the most to the least offensive
                for line_up in SORTED_LINE_UPS:
                    try:
                        self._validate_line_up(candidate_playing_players, line_up)
                        playing_players = candidate_playing_players.copy()
                        # found the proper line-up
                        logger.info(
                            f"{line_up} is valid for: {candidate_playing_players}"
                        )
                        if len(candidate_captain_substitute_id):
                            if line_up != self.line_up:  # use subsitute order
                                captain_substitute_id = candidate_substitutes_ids[0]
                            else:  # use the found id
                                captain_substitute_id = candidate_captain_substitute_id
                        line_up_found = True
                        break
                    except InvalidTeamLineup:
                        logger.debug(
                            f"{line_up} is invalid for: {candidate_playing_players}"
                        )
            if len(captain_substitute_id) and captain_to_be_substituted:
                playing_players.loc[:, "captain"] = (
                    playing_players["_id"] == captain_substitute_id
                )
            logger.info(f"Final list: {playing_players}")
        # compute the points
        points = 0.0 if is_away else HOME_BONUS
        for _, player in playing_players.iterrows():
            points += CAPTAIN_MODIFIER * player["points"] if player["captain"] else player["points"]
        return np.round(points, 2)
