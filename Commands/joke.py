# https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Fun/joke.js

from random import choice
from requests import get, RequestException

defaultAPIList = [
  {'name': 'jokeAPI', 'link': 'https://v2.jokeapi.dev', 'url': 'https://v2.jokeapi.dev/joke/Any'},
  {'name': 'humorAPI', 'link': 'https://humorapi.com', 'url': 'https://api.humorapi.com/jokes/random'},
  {'name': 'icanhazdadjoke', 'link': 'https://icanhazdadjoke.com', 'url': 'https://icanhazdadjoke.com'}
]

def getJoke(APIList=[], jokeType='', maxLength=2000) -> tuple[str, dict[str, str]]:
  if not APIList: APIList = defaultAPIList

  API = choice(APIList)
  response = None

  try:
    if API['name'] == 'jokeAPI':
      res = get(f"{API['url']}?lang=en", timeout=2.5).json()
      if res['type'] == 'twopart':
        response = f"{res['setup']}\n\n{res['delivery']}"
      else:
        response = res['joke']

    # elif API['name'] == 'humorAPI':
    #   res = get(f"{API['url']}?api-key={this.keys.humorAPIKey}&min-rating=7&max-length={maxLength}&include-tags={type}", timeout=2.5).json()
    #   if 'Q: ' in res['joke']:
    #     response = res['joke'].replace('Q: ', '').replace('A: ', '\n||') + '||\n'
    #   else:
    #     response = res['joke']

    elif API['name'] == 'icanhazdadjoke':
      res = get(API['url'], headers={'Accept': 'application/json'}).json()
      response = res['joke']
  except RequestException as err:
    if err.response and err.response.status_code in [402, 403, 522]:
      print('joke.py:', err.response.text)
    elif err.response:
      print(f"joke.py: {API['url']} responded with error {err.response.status_code}, {err.response.reason}: {err.response.text}")
    else:
      print(f"joke.py: {API['url']} responded with error: {err}")

  if isinstance(response, str):
    return response.replace('`', "'"), API

  APIList = [api for api in APIList if api['name'] != API['name']]
  if APIList:
    return getJoke(APIList, jokeType, maxLength)
  return '', {}


def joke(jokeType: str='', maxLength: int=2000):
  joke, API = getJoke(defaultAPIList, jokeType, maxLength)

  if not joke: return 'noAPIAvailable'
  return f"{joke}\n- {API['name']} ({API['link']})"

if __name__ == '__main__': print(joke())