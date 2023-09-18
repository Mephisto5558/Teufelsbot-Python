# https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Fun/joke.js

from secrets import choice

from requests import RequestException, get

from utils import log, Command, Cooldowns, Option

default_api_list = [
    {'name': 'jokeAPI', 'link': 'https://v2.jokeapi.dev', 'url': 'https://v2.jokeapi.dev/joke/Any'},
    {'name': 'humorAPI', 'link': 'https://humorapi.com', 'url': 'https://api.humorapi.com/jokes/random'},
    {'name': 'icanhazdadjoke', 'link': 'https://icanhazdadjoke.com', 'url': 'https://icanhazdadjoke.com'}
]

def get_joke(api_list=None, joke_type: str | None = '', blacklist: str | None = '', max_length=2000) -> tuple[str, dict[str, str]]:
  if api_list is None: api_list = default_api_list

  api = choice(api_list)
  response = None

  try:
    if api['name'] == 'jokeAPI':
      res = get(f"{api['url']}?lang=en&blacklist={blacklist}", timeout=2.5).json()
      if res['type'] == 'twopart':
        response = f"{res['setup']}\n\n{res['delivery']}"
      else:
        response = res['joke']

    # elif api['name'] == 'humorAPI':
    #   res = get(f"{api['url']}?api-key={this.keys.humorAPIKey}&min-rating=7&max-length={max_length}&include-tags={type}&exclude-tags={blacklist}", timeout=2.5).json()
    #   if 'Q: ' in res['joke']:
    #     response = res['joke'].replace('Q: ', '').replace('A: ', '\n||') + '||\n'
    #   else:
    #     response = res['joke']

    elif api['name'] == 'icanhazdadjoke':
      res = get(api['url'], headers={'Accept': 'application/json'}, timeout=10).json()
      response = res['joke']
  except RequestException as err:
    if err.response and err.response.status_code in [402, 403, 522]:
      log.error(err.response.text)
    elif err.response:
      log.error(
          '%s responded with error %i, %s: %s',
          api['url'], err.response.status_code, err.response.reason, err.response.text
      )
    else:
      log.error('%s responded with error: %s', api['url'], err)

  if isinstance(response, str):
    return response.replace('`', "'"), api

  api_list = [e for e in api_list if e['name'] != api['name']]
  if api_list:
    return get_joke(api_list, joke_type, blacklist, max_length)
  return '', {}

class CMD(Command):
  name = 'joke'
  cooldowns = Cooldowns(guild=100)
  slash_command = True
  prefix_command = True
  dm_permission = True
  options = [
      Option(name='api', type='String', autocomplete_options=[e['name'] for e in default_api_list], strict_autocomplete=True),
      Option(name='type', type='String'),
      Option(name='blacklist', type='String', choices=['nsfw', 'religious', 'political', 'racist', 'sexist', 'explicit']),
      Option(name='max_length', type='Integer', min_value=10, max_value=2000)
  ]

  def run(self, msg, lang):
    api = msg.options.get_string('api')
    joke_type = msg.options.get_string('type') or msg.args[0] if msg.args else None
    blacklist = msg.options.get_string('blacklist')
    max_length = msg.options.get_integer('max_length')
    joke_msg, api = get_joke(
        api_list=[e['name'] for e in default_api_list if e['name'] == api] if api else default_api_list,
        joke_type=joke_type,
        blacklist=blacklist,
        max_length=max_length
    )

    if not joke_msg: return msg.custom_reply(lang('no_api_available'))
    return msg.custom_reply(f"{joke_msg}\n- {api['name']} ({api['link']})")
