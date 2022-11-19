# Result_Finder.py

from serpapi import GoogleSearch
import pprint
params = {
  "q": "Argentina",
  "api_key": "11c415ed489cd6c54fcd546fbcbad344c88e7ce4ed3a4f96b4460024da51fe23"
}

search = GoogleSearch(params)
results = search.get_dict()
sports_results = results["sports_results"]
print(sports_results)