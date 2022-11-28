from serpapi import GoogleSearch
import pprint

API_KEY = "11c415ed489cd6c54fcd546fbcbad344c88e7ce4ed3a4f96b4460024da51fe23"
params = {
    "q": "Giants",
    "api_key": API_KEY,
    "hl": "en"
}

# search = GoogleSearch(params)
# results = search.get_dict()
# sports_results = results["sports_results"]
# pprint.pp(sports_results)

def get_recent_result(team: str, national_team_soccer: bool):
    """Gets recent match result."""
    params = {
        "q": team,
        "api_key": API_KEY
    }

    if national_team_soccer:
        params["q"] += " national soccer"

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        sports_results = results["sports_results"]
        result = f"The {team} "
        if "game_spotlight" in sports_results:
            spotlight = sports_results["game_spotlight"]
            date = spotlight["date"]
            enemy = spotlight["teams"][0]['name']
            flipped = False
            if enemy == sports_results["title"]:
                enemy = spotlight["teams"][-1]['name']
                flipped = True

            if ',' in date:
                result += f"are playing {enemy} on {date}."
            else:
                score = [ spotlight["teams"][-1]['score']['total'], spotlight["teams"][0]['score']['total']]
                if flipped:
                    score = score[::-1]
                outcome = "winning" if score[0] > score[-1] else "losing"
                if spotlight['league'] == date:
                    result += f"are current playing {enemy}, {outcome} {score[0]} to {score[-1]}."
                else:
                    result += f"played against {enemy} on {date}, {outcome} {score[0]} to {score[-1]}."
        else:
            result += "didn't play any games recently and aren't playing very soon."
        return result
    
    # result = "The {team} played against {enemy}, winning/losing score to score"

    except KeyError:
        return "Couldn't find a recent score."

    except Exception:
        return "Unknown error occurred."