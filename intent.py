from dataclasses import dataclass

@dataclass
class Intent:
    """Intents for our """
    TRADE: str = "trade OR headed OR sold OR transfer"
    INJURY: str = "injury OR hurt OR benched"
    PROFILE: str = "profile OR account"
    FAVORITE: str = "favorite AND teams OR players"

INTENTS = [Intent.TRADE, Intent.INJURY, Intent.PROFILE, Intent.FAVORITE]
