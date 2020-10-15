class ParsingException(Exception):
    pass


class EnvVariableNotSet(Exception):
    def __init__(self, varname: str):
        super(EnvVariableNotSet, self).__init__(f"Env variable [{varname}] not set.")
