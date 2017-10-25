from enum import Enum, unique, auto

@unique # pylint: disable=invalid-name
class SHEPHERD_HEADER(Enum):
    GOAL_SCORE = auto()
    GOAL_BID = auto()
    CODE_INPUT = auto()

    START_MATCH = auto()
    SETUP_MATCH = auto()
    START_NEXT_STAGE = auto()
    RESET_CURRENT_STAGE = auto()
    RESET_MATCH = auto()

    BID_TIMER_END = auto()
    STAGE_TIMER_END = auto()

@unique # pylint: disable=invalid-name
class SENSOR_HEADER(Enum):
    CODE_RESULT = auto()
    FAILED_POWERUP = auto()
    CURRENT_BID = auto()

@unique # pylint: disable=invalid-name
class SCOREBOARD_HEADER(Enum):
    SCORE = auto()
    TEAMS = auto()
    BID_TIMER_START = auto()
    BID_AMOUNT = auto()
    BID_WIN = auto()
    STAGE = auto()
    STAGE_TIMER_START = auto()
    POWERUPS = auto()
    ALLIANCE_MULTIPLIER = auto()

@unique # pylint: disable=invalid-name
class CONSTANTS(Enum):
    TWO_X_COOLDOWN = 1
    ZERO_X_COOLDOWN = 1
    STEAL_COOLDOWN = 1
    CODE_COOLDOWN = 1
    BID_INCREASE_CONSTANT = 1

@unique # pylint: disable=invalid-name
class TIMER_TYPES(Enum):
    BID = 'bid'
    MATCH = 'match'
    COOLDOWN = 'cooldown'
    CODE_COOLDOWN = 'code_cooldown'
    DURATION = 'duration'
