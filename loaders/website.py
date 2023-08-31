from functools import partial
from importlib import import_module
from os import listdir, path
from re import IGNORECASE, sub
from sys import argv
from time import sleep

from flask import Flask, jsonify, make_response, request
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from utils import git_pull, i18n_provider

lang = partial(i18n_provider.__, locale='en', none_not_found=True)
owner_only_folders = []
def validate(key: str, website_key: str):
  """Returns false if everything is alright"""
  if key != website_key:
    return make_response({'message': 'You need to provide a valid "key" url parameter to access this information.'}, 401)
  return False

def get_commands() -> list[dict[str, str | bool | list[dict[str, str]]]]:
  category_command_list = []
  for subfolder in listdir('commands'):
    if subfolder.lower() in owner_only_folders: continue

    command_list: list[dict[str, str]] = []
    for cmd_file in listdir(f'commands/{subfolder}'):
      if not cmd_file.endswith('.py'): continue

      cmd = import_module(f'commands.{subfolder}.{path.splitext(cmd_file)[0]}')
      if not cmd or not cmd.name or cmd.disabled: continue

      prefix_list = ', '.join(cmd.aliases.prefix) if cmd.aliases and cmd.aliases.prefix else ''
      slash_list = ', '.join(cmd.aliases.slash) if cmd.aliases and cmd.aliases.slash else ''
      lang_path = f'commands.{subfolder.lower()}.{cmd.name}'

      command_list.append({
          'command_name': cmd.name,
          'command_usage':
              ('SLASH Command: Look at the option descriptions.\n' if cmd.slash_command else '')
              + sub('slash command:', '', lang(f'commands.{lang_path}.usage.usage') or '', flags=IGNORECASE)  # NOSONAR (false positive)
              or 'No information found',
          'command_description': cmd.description or lang(f'commands.{lang_path}.description') or 'No information found',
          'command_alias':
              (f'Prefix: {prefix_list}\n' if prefix_list else '')
              + (f'Slash: {slash_list}\n' if slash_list else '')
              or str(lang('global.none'))
      })

    category_command_list.append({
        'category': subfolder,
        'sub_title': '',
        'aliases_disabled': not any(e['command_alias'] for e in command_list),
        'list': [{k: v.strip().replace('\n', '<br>&nbsp') for k, v in e.items()} for e in command_list]
    })

  category_command_list.sort(key=lambda e: (e.category.lower() == 'others', len(e.list)))
  return category_command_list

commands = get_commands()
WEBSITE_KEY = 'x'

def website_handler(client):
  while 'is_child=True' in argv: sleep(.5)  # Waiting for slash command loader to finish so parent process ends to free the port

  app = Flask(__name__)
  csrf = CSRFProtect()
  csrf.init_app(app)
  limiter = Limiter(key_func=get_remote_address, app=app)

  @app.route('/')
  @limiter.limit('10/second')
  def ratelimit_handler():
    return jsonify({'message': 'Sorry, you have been ratelimited!'}), 429

  @app.route('/commands')
  @limiter.limit('10/second')
  def commands_():
    return validate(request.args.get('key') or '', WEBSITE_KEY) or jsonify(get_commands() if request.args.get('fetch') else commands)

  @app.route('/reloadDB')
  @limiter.limit('10/second')
  def reload_db():
    valid = validate(request.args.get('key') or '', WEBSITE_KEY)
    if valid: return valid

    client.db.fetch(request.args.get('db'))
    return jsonify({'message': 'OK'}), 200

  @app.route('/git/pull')
  @limiter.limit('1/second')
  def gitpull():
    git_pull()
    return jsonify({'message': 'OK'}), 200

  @app.route('/')
  def home():
    return jsonify({'message': 'OK'}), 200

  @app.errorhandler(404)
  def page_not_found(_):
    return jsonify({'message': 'Not Found'}), 404

  app.run(port=8000)
