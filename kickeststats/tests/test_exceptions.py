"""Testing exception utilities."""
import pytest

from ..exceptions import (
    EnvVariableNotSet,
    InvalidLineUp,
    InvalidTeamLineup,
    ParsingException,
    UnsupportedLineUp,
)


def test_parsing_exception():
    with pytest.raises(Exception):
        raise ParsingException("A parsing error.")


def test_env_variable_not_set():
    with pytest.raises(Exception):
        exception = EnvVariableNotSet("VARIABLE")
        assert str(exception) == "Env variable [VARIABLE] not set."
        raise exception


def test_invalid_line_up():
    with pytest.raises(Exception):
        raise InvalidLineUp("An invalid line-up error.")


def test_unsupported_line_up():
    with pytest.raises(Exception):
        exception = UnsupportedLineUp("X-X-X")
        assert str(exception) == "Line-up [X-X-X] is not supported."
        raise exception


def test_invalid_team_line_up():
    with pytest.raises(Exception):
        raise InvalidTeamLineup("An invalid team line-up error.")
