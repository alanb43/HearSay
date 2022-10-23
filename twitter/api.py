import requests
import os
import json
import config

# Ask Josh for the config file for the Twitter Dev keys, not putting them on github for obvious reasons
bearer_token = config.BEARER_TOKEN

# Twitter API Sample Code
# https://github.com/twitterdev/Twitter-API-v2-sample-code

# Play with Twitter API without writing code
# https://oauth-playground.glitch.me/?id=listIdGet&params=%28%27id%21%271409935014725177344%27%29_


#### ONLY CHANGE SEARCH_URL & QUERY_PARAMS TO MAKE DIFFERENT API CALLS, REST UNCHANGED ###################

# Which endpoint we want to hit
search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': 'Cristiano Ronaldo'}

##########################################################################################################
#### ONCE WORKING, DO NOT TOUCH CODE BELOW ###############################################################


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()