from data_classes.user_profile import UserProfile, ProfileSetupState
from sentiment_classifier import find_adjective

from random import randrange

class ProfileManager:
    """Manages everything for user profiles."""
    def __init__(self, input_analyzer, sentiment_classifier, tweet_snagger, response_gen):
        self.input_analyzer = input_analyzer
        self.sentiment_classifier = sentiment_classifier
        self.tweet_snagger = tweet_snagger
        self.profile : UserProfile = None
        self.response_gen = response_gen
        self.reset_profile()

    def profile_exists(self) -> bool:
        """Returns whether a profile has been set up."""
        return self.profile is not None

    def reset_profile(self) -> None:
        """Resets profile and profile setup state."""
        self.create_profile_state = ProfileSetupState(False, "", "", "")

    def build_profile(self, utterance):
        """Uses data aggregated from back-end to construct UserProfile."""
        response = ""
        if self.create_profile_state.name == "":
            name: str = self.input_analyzer.extract_entities(utterance)[0]["word"].title()
            self.create_profile_state.name = name
            response = f"Nice to meet you, {name}. Which teams do you support?"
        elif len(self.create_profile_state.teams) == 0:
            teams = [str(e['word']).title() for e in self.input_analyzer.extract_entities(utterance)]
            self.create_profile_state.teams = teams
            response = f"Ah, a {teams[0]} fan I see. Have any favorite players?"
        elif len(self.create_profile_state.players) == 0:
            players = [e['word'] for e in self.input_analyzer.extract_entities(utterance)]
            self.create_profile_state.players = players
            self.profile = UserProfile(
                user=self.create_profile_state.name,
                teams=self.create_profile_state.teams,
                players=self.create_profile_state.players
            )
            self.create_profile_state.engaged = False
            response =  "Got it. I've set up your profile!"
        
        return response
    
    def get_info_about_favorites(self, teams: bool):
        choice = ""
        if teams:
            team_choice = randrange(0, len(self.profile.teams))
            choice = self.profile.teams[team_choice]
        else:
            player_choice = randrange(0, len(self.profile.players))
            choice = self.profile.players[player_choice]
        
        tweet_objects = self.tweet_snagger.snag_tweets([choice], intent="other", num_tweets=15)
        tweets = [tweet['content'] for tweet in tweet_objects]
        sentiment = self.sentiment_classifier.batch_analysis(tweets)["sentiment"]
        adjective = find_adjective(sentiment)
        data = self.response_gen.summarize_text(tweets)[0]["summary_text"]
        speech = "Overall, it seems like "
        if teams:
            speech += f" the {choice} team is doing {adjective} lately."
        else:
            speech += f" {choice} has been playing {adjective} recently."
        
        speech += f" Here's a quick summary: {data}"
        return speech
