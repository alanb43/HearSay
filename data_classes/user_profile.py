from dataclasses import dataclass

@dataclass
class UserProfile:
    """Representation of a user profile."""
    user: str
    teams: list
    players: list

@dataclass
class ProfileSetupState:
    """State for profile creation process."""
    engaged: bool
    name: str
    teams: list
    players: list
