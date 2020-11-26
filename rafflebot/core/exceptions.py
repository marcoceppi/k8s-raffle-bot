class RaffleBotException(Exception):
    pass


class DatabaseEngineException(RaffleBotException):
    pass


class EngineNotFound(DatabaseEngineException):
    pass
