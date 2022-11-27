from dataclasses import dataclass

@dataclass
class Intent:
    """Intents for our """
    TRADE: str = "trade OR headed OR sold OR transfer"
    INJURY: str = "injury OR injured OR hurt OR benched"

INTENTS = [Intent.TRADE, Intent.INJURY]
