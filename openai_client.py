import openai

ENGINE = 'curie'

NL = '\n'

class OpenAIClient:
    """Uses OpenAI for sentiment analysis"""

    def __init__(self, api_key: str):
        openai.api_key = api_key

    def player_has_injury(self, player: str, tweet: str) -> bool:
        prompt = f"Sentiment Analyzer (Yes/No).{NL}{tweet}{NL}Does {player} have an injury: "
        completion = openai.Completion.create(engine=ENGINE, prompt=prompt)
        print(completion)
        text: str = completion.choices[0].text
        print('Prompt:', '^', prompt, '$')
        print('Completion:', '^', text, '$')
        return text.lower().find('yes') != -1
    
    def query(self, prompt: str) -> str:
        completion = openai.Completion.create(engine=ENGINE, prompt=prompt)
        return completion.choices[0].text