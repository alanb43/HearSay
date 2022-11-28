from dataclasses import dataclass

@dataclass
class UserProfile:
    """Representation of a user profile."""
    user: str
    teams: list
    players: list
