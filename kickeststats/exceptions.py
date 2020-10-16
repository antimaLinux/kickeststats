"""Exception utilities."""


class ParsingException(Exception):
    pass


class EnvVariableNotSet(Exception):
    def __init__(self, varname: str) -> None:
        super(EnvVariableNotSet, self).__init__(f"Env variable [{varname}] not set.")


class InvalidLineUp(Exception):
    pass


class UnsupportedLineUp(Exception):
    def __init__(self, line_up_name: str) -> None:
        super(UnsupportedLineUp, self).__init__(f"Line-up [{line_up_name}] is not supported.")


class InvalidTeamLineup(Exception):
    pass
