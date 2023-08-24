# https://github.com/Mephisto5558/Teufelsbot/blob/main/index.js

from time import process_time_ns
from json import load
from os import environ, listdir
from importlib import import_module

from utils import DB, log, box

init_time = process_time_ns() / 1e6
log.info('Initializing time: %fms', init_time)

# git_pull()

class Client(dict):
  """This will be discord client obj at some point"""

  def __init__(self):
    try:
      with open('env.json', 'r', encoding='utf8') as file:
        self.env = box.from_json(load(file))
    except FileNotFoundError:
      self.env = box

    self.db = DB(str(self.env.get('dbConnectionStr', environ.get('dbConnectionStr', ''))))

    if not self.env: self.env = self.settings.get('env', box)

    self.bot_type = self.env.get('environment', 'main')

  @property
  def settings(self):
    data = self.db.get('botSettings')
    return data if isinstance(data, box.__class__) else box

client = Client()

for loader in listdir('./loaders'):
  if client.bot_type != 'dev' or 'website' not in loader:
    module = import_module(f'loaders.{loader[:-3]}')
    module.main(client)

# client.login()
log.info('Logged into %s', client.bot_type)

client.db.set('botSettings', f'startCount.{client.bot_type}', client.settings.get(f'startCount.{client.bot_type}', 0) + 1)
