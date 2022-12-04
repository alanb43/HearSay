from dataclasses import dataclass

@dataclass
class Intents:
    """Different intents we intend the bot to act upon."""
    TRADE: str = "trade OR headed OR sold OR transfer"
    INJURY: str = "injury OR injured OR hurt OR benched"
    PROFILE: str = "(create OR make) AND (profile OR account)"
    FAV_TEAMS: str = "favorite AND (team OR teams)"
    FAV_PLAYERS: str = "favorite AND (player OR players)"

INTENTS = [
    Intents.TRADE, 
    Intents.INJURY,
    # Intents.PROFILE,
    # Intents.FAV_TEAMS,
    # Intents.FAV_PLAYERS
]

# trade OR headed OR sold OR transfer, injury OR injured OR hurt OR benched, (create OR make) AND (profile OR account), favorite AND (team OR teams), favorite AND (player OR players)
