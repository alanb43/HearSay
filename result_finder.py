from serpapi import GoogleSearch
import pprint

API_KEY = "11c415ed489cd6c54fcd546fbcbad344c88e7ce4ed3a4f96b4460024da51fe23"
params = {
    "q": "dallas mavericks",
    "api_key": API_KEY
}

search = GoogleSearch(params)
results = search.get_dict()
sports_results = results["sports_results"]
pprint.pp(sports_results)

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

            if ',' in date:
                result += f" are playing {date} "
            else:
                result += f" played {date} "
        # else:
    
    # result = "The {team} played against {enemy}, winning/losing score to score"

    except KeyError:
        return "Couldn't find a recent score."

    except Exception:
        return "Unknown error occurred."
