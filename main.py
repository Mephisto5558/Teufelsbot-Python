from time import process_time_ns
from json import load
from os import environ, listdir
from importlib import import_module

from config import logger, FlatDict
from Utils.db import DB

init_time = process_time_ns() / 1e6
logger.info('Initializing time: %fms', init_time)

# git_pull()

class Client(dict):
  """This will be discord client obj at some point"""

  def __init__(self):
    try:
      with open('env.json', 'r', encoding='utf8') as file:
        self.env = FlatDict(load(file))
    except FileNotFoundError:
      self.env = FlatDict()

    self.db = DB(self.env.get('dbConnectionStr', environ['dbConnectionStr'], ''))

    if not self.env: self.env = self.settings.get('env', FlatDict())

    self.bot_type = self.env.get('environment', 'main')

  @property
  def settings(self):  # pylint: disable=unsubscriptable-object
    return self.db.get('botSettings')

client = Client()

for handler in listdir('./Handlers'):
  if client.bot_type != 'dev' or 'website' not in handler:
    module = import_module(f'Handlers.{handler[:-3]}')
    module.main(client)

client.db.set('botSettings', f'startCount.{client.bot_type}', client.settings.get(f'startCount.{client.bot_type}', 0) + 1)


breakpoint()
