from data_classes.user_profile import UserProfile

from random import randrange

class ProfileManager:
    """Manages everything for user profiles."""
    
    def __init__(self, speech_manager, input_analyzer, 
                 sentiment_classifier, tweet_snagger):
        self.speech_manager = speech_manager
        self.input_analyzer = input_analyzer
        self.sentiment_classifier = sentiment_classifier
        self.tweet_snagger = tweet_snagger
        self.profile : UserProfile = None

    def create_profile(self) -> UserProfile:
        """Gathers and analyzes verbal input to make a user profile."""
        self.speech_manager.text_to_speech("What's your name?")
        name = self.speech_manager.speech_to_text()
        teams_q = f"Nice to meet you, {name}. Which teams do you support?"
        self.speech_manager.text_to_speech(teams_q)
        teams_input = self.speech_manager.speech_to_text()
        teams = [e['word'] for e in self.input_analyzer.extract_entities(teams_input)]
        players_q = f"Ah, a {teams[0]} fan I see. Have any favorite players?"
        self.speech_manager.text_to_speech(players_q)
        players_input = self.speech_manager.speech_to_text()
        players = [e['word'] for e in self.input_analyzer.extract_entities(players_input)]
        self.speech_manager.text_to_speech("Got it. I've set up your profile!")
        self.profile = UserProfile(name,teams,players)
    
    def get_info_about_favorites(self, teams: bool):
        if teams:
            team_choice = randrange(0, len(self.profile.teams))
            team = self.profile.teams[team_choice]
            tweets = self.tweet_snagger.snag_tweets([team], intent="other", num_tweets=15)
            
        else:
            player_choice = randrange(0, len(self.profile.players))
            player = self.profile.players[player_choice]
            tweets = self.tweet_snagger.snag_tweets([player], intent="other", num_tweets=15)

        analysis = self.sentiment_classifier.batch_analysis(tweets)

        if type(analysis) != dict:
            return ""
            
        speech = "Overall, it seems like "
        sentiment = analysis["sentiment"]
        adjective = self.sentiment_classifier.find_adjective(sentiment)
        if team:
            speech += f" the {team} team is doing {adjective} lately"
        else:
            speech += f" {player} has playing {adjective} recently"
        
        return speech
