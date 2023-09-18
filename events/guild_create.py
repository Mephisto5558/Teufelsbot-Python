from utils import log

def run(guild):
  log.debug('Joined new guild: %s', guild.id)
  if guild.client.bot_type == 'dev': return

  settings = guild.client.db.get('GUILDSETTINGS')
  guild.client.db.set('GUILDSETTINGS', f'{guild.id}.position', (max((e.get('position', 0) for e in settings.values()), default=0) + 1) if settings else 1)