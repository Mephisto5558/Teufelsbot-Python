from requests import get

from utils import Command, Cooldowns

class Fact(Command):
  name = 'fact'
  cooldowns = Cooldowns(guild=100)
  slash_command = True
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    res = get(f'https://uselessfacts.jsph.pl/api/v2/facts/random?language={lang}', timeout=10).json()
    if not res['text']: return None

    return msg.custom_reply(f"{res['text']}\n\nSource: [{res['source']}]({res['source_url']})")
