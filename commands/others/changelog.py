from utils import Aliases, Command, Cooldowns, Colors

class CMD(Command):
  name = 'changelog'
  aliases = Aliases(prefix=['changelogs'])
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    embed = EmbedBuilder(title=lang('embed_title'), description=msg.client.settings.changelog or lang('none_found'), color=Colors.White)
    return msg.custom_reply(embeds=[embed])
