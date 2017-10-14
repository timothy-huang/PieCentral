from enum import Enum, unique

class Header(Enum):
    # Used to autoenumerate
    def __new__(cls):
        value = len(cls.__members__) + 1 # pylint: disable=no-member
        obj = object.__new__(cls)
        obj._value_ = value # pylint: disable=protected-access
        return obj

@unique
class SHEPHERD_HEADER(Header): # pylint: disable=invalid-name
    GOAL_SCORE = ()
    GOAL_BID = ()
    CODE_INPUT = ()

    START_MATCH = ()
    SETUP_MATCH = ()
    START_NEXT_STAGE = ()
    RESET_CURRENT_STAGE = ()
    RESET_MATCH = ()

    BID_TIMER_END = ()
    STAGE_TIMER_END = ()

@unique
class SENSOR_HEADER(Header): # pylint: disable=invalid-name
    CODE_RESULT = ()
    FAILED_POWERUP = ()
    CURRENT_BID = ()

@unique
class SCOREBOARD_HEADER(Header): # pylint: disable=invalid-name
    SCORE = ()
    TEAMS = ()
    BID_TIMER_START = ()
    BID_AMOUNT = ()
    BID_WIN = ()
    STAGE = ()
    STAGE_TIMER_START = ()
    POWERUPS = ()
    ALLIANCE_MULTIPLIER = ()
