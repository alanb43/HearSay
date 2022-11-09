import openai

INJURY_QUERY = \
"""Sentiment Analyzer (Yes/No).

%s

Does %s have an injury:"""

class OpenAIClient:
    """Uses OpenAI for sentiment analysis"""

    def __init__(self, api_key: str):
        openai.api_key = api_key

    def player_has_injury(self, player: str, tweet: str) -> bool:
        prompt = INJURY_QUERY % (tweet, player)
        completion = openai.Completion.create(engine='davinci', prompt=prompt)
        print(completion)
        text: str = completion.choices[0].text
        print('Prompt:', '^', prompt, '$')
        print('Completion:', '^', text, '$')
        return text.lower().find('yes') != -1
