from __future__ import annotations
from typing import TYPE_CHECKING

from discord import Guild

from utils import log
if TYPE_CHECKING:
  from main import MyClient

def run(client: MyClient, guild: Guild):
  log.debug('Joined new guild: %s', guild.id)
  if client.bot_type == 'dev': return

  settings = client.db.get('GUILD_SETTINGS')
  client.db.set(
      'GUILD_SETTINGS',
      f'{guild.id}.position',
      (max((e.get('position', 0) for e in settings.values()), default=0) + 1) if settings else 1
  )
