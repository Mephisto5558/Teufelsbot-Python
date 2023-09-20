from importlib import import_module
from os import environ, listdir
from sys import exit  # pylint:disable=redefined-builtin
from time import process_time_ns
import asyncio

from discord import AllowedMentions, Client, Intents, Activity, ActivityType
from oracledb import OperationalError

from utils import DB, Box, box, git_pull, log, Command

init_time = process_time_ns() / 1e6
log.info('Initializing time: %fms', init_time)

class MyClient(Client):
  def __init__(self):
    super().__init__(
        shards='auto',
        allowed_mentions=AllowedMentions(everyone=False, users=True, roles=True),
        intents=Intents(
            guilds=True,
            members=True,
            messages=True,
            reactions=True,
            voice_states=True,
            message_content=True,
            dm_messages=True
        ),
        partials=['channel', 'message', 'reaction']
    )

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

    if self.settings.activity: activity = Activity(**self.settings.activity)
    else: activity = Activity(name='/help', type=ActivityType.playing)

    self.change_presence(activity=activity)

  prefix_commands: dict[str, Command] = {}
  slash_commands: dict[str, Command] = {}
  cooldowns: dict[str, dict[str, dict[str, int]]] = {'guild': {}, 'user': {}}

  @property
  def settings(self):
    data = self.db.get('BOT_SETTINGS')
    return data if isinstance(data, Box) else box()

  @property
  def default_settings(self):
    data = self.db.get('GUILD_SETTINGS')
    return data.default if isinstance(data, Box) else box()

  @default_settings.setter
  def default_settings(self, val):
    self.db.set('GUILD_SETTINGS', 'default', val)

async def main():
  result = await git_pull()
  if result != 'OK' and 'Could not resolve host' in result:
    log.error('It seems like the bot does not have internet access.')
    exit(1)

  client = MyClient()

  for loader in listdir('./loaders'):
    if client.bot_type != 'dev' or 'website' not in loader:
      module = import_module(f'loaders.{loader[:-3]}')
      if module.main and callable(module.main): module.main(client)

  await client.login(client.env[client.env.bot_type].token)
  log.info('Logged into %s', client.bot_type)

  client.db.set('BOT_SETTINGS', f'startCount.{client.bot_type}', client.settings.get(f'startCount.{client.bot_type}', 0) + 1)

asyncio.run(main())
