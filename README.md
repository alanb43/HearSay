# HearSay: a conversational sports insider

## Background 
HearSay makes staying on top of your favorite sports teams and players easy with user profiles and fluid question and answering. See our [live demo](https://youtu.be/XhzURple008?t=301) to get a feel for what HearSay can do! <br>
## Development
To use and tinker with HearSay locally, follow these steps:

1. Clone this repository
2. Determine whether you want to use our fine-tuned sentiment-analyzation & entity-extraction models, or if you'd rather use the base models via the [HuggingFace API](https://huggingface.co/docs/api-inference/quicktour).
3. If fine-tuned, reach out to bera@umich.edu for access to the files (we don't host them in this repo). Then, in your local project directory create an environment variable using: 
  ```bash
  export FINE_TUNED=1
  ```

If API, create the following environment variables instead:
```bash
export FINE_TUNED=0
export HUGGINGFACE_API_KEY="api key you create using link above"
```

4. In either case, you need to create a [serp api key](https://serpapi.com/) and create an environment variable using
```bash
export SERP_API_KEY="api key"
```
5. With these prerequisites met, you can run HearSay using these commands in separate shell windows:
```Python
# back-end
python3 -m venv env
source env/bin/activate && pip3 install -r requirements.txt
python3 main.py
```
```JavaScript
// front-end
cd hearsay-client
npm install
npm start
```
6. Navigate to localhost:3000 and start using HearSay!


