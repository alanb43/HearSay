from dataclasses import dataclass

@dataclass
class Intent:
    """Intents for our """
    TRADE: str = "trade"
    INJURY: str = "injury"

INTENTS = [Intent.TRADE, Intent.INJURY]
