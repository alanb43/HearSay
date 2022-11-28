from dataclasses import dataclass

@dataclass
class Intents:
    """Different intents we intend the bot to act upon."""
    TRADE: str = "trade OR headed OR sold OR transfer"
    INJURY: str = "injury OR injured OR hurt OR benched"
    PROFILE: str = "profile OR account"
    FAV_TEAMS: str = "favorite AND team"
    FAV_PLAYERS: str = "favorite AND player"

INTENTS = [
    Intents.TRADE, 
    Intents.INJURY,
    Intents.PROFILE,
    Intents.FAV_TEAMS,
    Intents.FAV_PLAYERS
]
