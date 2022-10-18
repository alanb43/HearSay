import requests
import os
import json


# TWITTER API - READ FIRST

# Here's a good place to play with the api so we can figure out what calls to make:
# https://oauth-playground.glitch.me/?id=tweetsRecentSearch&params=%28%27query%21%27from%3A+FabrizioRomano%27%29_

# This is the Github for the entire API with samples:
# https://github.com/twitterdev/Twitter-API-v2-sample-code

# Need HearSay Twitter Developer Project Keys to authenticate, keys not getting committed to Github so ask Josh for keys

# Currently can't get following code to authenticate, it's returning a 401

os.system('chmod +x config.sh')
os.system('./config.sh')
bearer_token = os.environ.get("BEARER_TOKEN")


######################################## THIS IS THE PART THAT CHANGES TO MAKE DIFFERENT API CALLS ##########################################
########## VISIT https://oauth-playground.glitch.me/?id=listIdGet&params=%28%27id%21%271409935014725177344%27%29_ TO PLAY WITH API ##########

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(from:FabrizioRomano)','tweet.fields': 'author_id'}

#############################################################################################################################################
########################## ONCE DEBUGGED NONE OF THE CODE BELOW SHOULD NEED TO BE TOUCHED TO MAKE DIFFERENT API CALLS #######################


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()