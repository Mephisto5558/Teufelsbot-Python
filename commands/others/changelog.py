from discord import Embed, Color

from utils import Aliases, Command, Cooldowns

class CMD(Command):
  name = 'changelog'
  aliases = Aliases(prefix=['changelogs'])
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = True
  dm_permission = True

  async def run(self, msg, lang):
    embed = Embed(title=lang('embed_title'), description=msg.client.settings.changelog or lang('none_found'), color=Color.white())
    return msg.custom_reply(embeds=[embed])
