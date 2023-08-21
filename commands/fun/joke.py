# https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Fun/joke.js

from random import choice
from requests import get, RequestException

default_api_list = [
    {'name': 'jokeAPI', 'link': 'https://v2.jokeapi.dev', 'url': 'https://v2.jokeapi.dev/joke/Any'},
    {'name': 'humorAPI', 'link': 'https://humorapi.com', 'url': 'https://api.humorapi.com/jokes/random'},
    {'name': 'icanhazdadjoke', 'link': 'https://icanhazdadjoke.com', 'url': 'https://icanhazdadjoke.com'}
]

def get_joke(api_list=None, joke_type='', max_length=2000) -> tuple[str, dict[str, str]]:
  if api_list is None: api_list = default_api_list

  api = choice(api_list)
  response = None

  try:
    if api['name'] == 'jokeAPI':
      res = get(f"{api['url']}?lang=en", timeout=2.5).json()
      if res['type'] == 'twopart':
        response = f"{res['setup']}\n\n{res['delivery']}"
      else:
        response = res['joke']

    # elif api['name'] == 'humorAPI':
    #   res = get(f"{api['url']}?api-key={this.keys.humorAPIKey}&min-rating=7&max-length={max_length}&include-tags={type}", timeout=2.5).json()
    #   if 'Q: ' in res['joke']:
    #     response = res['joke'].replace('Q: ', '').replace('A: ', '\n||') + '||\n'
    #   else:
    #     response = res['joke']

    elif api['name'] == 'icanhazdadjoke':
      res = get(api['url'], headers={'Accept': 'application/json'}, timeout=10).json()
      response = res['joke']
  except RequestException as err:
    if err.response and err.response.status_code in [402, 403, 522]:
      print('joke.py:', err.response.text)
    elif err.response:
      print(
          f"joke.py: {api['url']} responded with error {err.response.status_code}, {err.response.reason}: {err.response.text}")
    else:
      print(f"joke.py: {api['url']} responded with error: {err}")

  if isinstance(response, str):
    return response.replace('`', "'"), api

  api_list = [api for api in api_list if api['name'] != api['name']]
  if api_list:
    return get_joke(api_list, joke_type, max_length)
  return '', {}


def joke(joke_type: str = '', max_length: int = 2000):
  joke_msg, api = get_joke(default_api_list, joke_type, max_length)

  if not joke_msg: return 'noAPIAvailable'
  return f"{joke_msg}\n- {api['name']} ({api['link']})"


if __name__ == '__main__': print(joke())
