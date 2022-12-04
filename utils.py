import os
import requests


FINE_TUNED = int(os.environ["FINE_TUNED"])
headers = {'Authorization': f'Bearer {os.environ["HUGGINGFACE_API_KEY"]}'}

def query(payload, url):
	response = requests.post(url, headers=headers, json=payload)
	return response.json()
