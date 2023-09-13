from requests import JSONDecodeError, get

from utils import Command, Cooldowns, log

class CMD(Command):
  name = 'inspirobot'
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    try:
      res = get('https://inspirobot.me/api?generate=true', timeout=10).json()
    except JSONDecodeError as err:
      msg.custom_reply(lang('error'))
      return log.error(err.args[0].message)

    if not res: return msg.custom_reply(lang('not_found'))

    embed = EmbedBuilder(image={'url': res.url}, footer={'text': '- inspirotbot.me'}, color='Random')

    return msg.custom_reply(embeds=[embed])
