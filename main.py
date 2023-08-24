# https://github.com/Mephisto5558/Teufelsbot/blob/main/index.js

from importlib import import_module
from json import load
from os import environ, listdir
from sys import exit
from time import process_time_ns

from utils import DB, Box, box, git_pull, log

result = git_pull()
if result != 'OK' and 'Could not resolve host' in result.stderr:
  print('It seems like the bot does not have internet access.')
  exit(1)

init_time = process_time_ns() / 1e6
log.info('Initializing time: %fms', init_time)

class Client(dict):
  """This will be discord client obj at some point"""

  def __init__(self):
    try:
      with open('env.json', 'r', encoding='utf8') as file:
        self.env = box().from_json(load(file))
    except FileNotFoundError:
      self.env = box()

    self.db = DB(str(self.env.get('dbConnectionStr', environ.get('dbConnectionStr', ''))))

    if not self.env: self.env = self.settings.env or box()

    self.bot_type = str(self.env.get('environment', 'main'))
    self.prefix_commands: list[dict] = []
    self.slash_commands: list[dict] = []
    self.cooldowns: dict[str, int] = {}

  @property
  def settings(self):
    data = self.db.get('botSettings')
    return data if isinstance(data, Box) else box()

client = Client()

for loader in listdir('./loaders'):
  if client.bot_type != 'dev' or 'website' not in loader:
    module = import_module(f'loaders.{loader[:-3]}')
    if module.main and callable(module.main): module.main(client)

# client.login()
log.info('Logged into %s', client.bot_type)

client.db.set('botSettings', f'startCount.{client.bot_type}', client.settings.get(f'startCount.{client.bot_type}', 0) + 1)
