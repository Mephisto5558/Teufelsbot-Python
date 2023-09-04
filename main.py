# https://github.com/Mephisto5558/Teufelsbot/blob/main/index.js

from importlib import import_module
from os import environ, listdir
from sys import exit  # pylint:disable=redefined-builtin
from time import process_time_ns

from oracledb import OperationalError

from utils import DB, Box, box, git_pull, log, Command

result = git_pull()
if result != 'OK' and 'Could not resolve host' in result.stderr:
  log.error('It seems like the bot does not have internet access.')
  exit(1)

init_time = process_time_ns() / 1e6
log.info('Initializing time: %fms', init_time)

class Client(dict):
  """This will be discord client obj at some point"""

  def __init__(self):
    try:
      self.env = box().from_json(filename='env.json', encoding='utf8')
    except FileNotFoundError:
      self.env = box()

    try:
      self.db = DB(
          str(self.env.get('dbConnectionStr', environ.get('dbConnectionStr', ''))),
          required_tables=['LEADERBOARDS', 'GIVEAWAYS', 'BOT_SETTINGS', 'USER_SETTINGS', 'GUILD_SETTINGS', 'POLLS']
      )
    except OperationalError as err:
      log.error('Error connecting to the database: %s', err)

    if not self.env: self.env = self.settings.env or box()

    self.bot_type = str(self.env.get('environment', 'main'))
    self.prefix_commands: dict[str, Command] = {}
    self.slash_commands: dict[str, Command] = {}
    self.cooldowns: dict[str, dict[str, dict[str, int]]] = {'guild': {}, 'user': {}}

  @property
  def settings(self):
    data = self.db.get('BOT_SETTINGS')
    return data if isinstance(data, Box) else box()

client = Client()

for loader in listdir('./loaders'):
  if client.bot_type != 'dev' or 'website' not in loader:
    module = import_module(f'loaders.{loader[:-3]}')
    if module.main and callable(module.main): module.main(client)

# client.login()
log.info('Logged into %s', client.bot_type)

client.db.set('BOT_SETTINGS', f'startCount.{client.bot_type}', client.settings.get(f'startCount.{client.bot_type}', 0) + 1)
