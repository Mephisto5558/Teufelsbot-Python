from secrets import choice

from discord import Embed, Color

from utils import Command, Cooldowns

images = [
    '1137786635392651314/backflip-anime.gif',
    '1137786636017602632/flip-anime.gif',
    '1137786636659335321/ichigo-mashimaro-backflip.gif',
    '1137786637162664106/pokemon-mew.gif',
    '1137786637573693561/neo-rwby.gif',
    '1137786637959581747/ezgif-5-7572493502.gif',
    '1137786638324469820/back-flip-attack-on-titan.gif']

class CMD(Command):
  name = 'flip'
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = True

  def run(self, msg, lang):
    embed = Embed(
        title=lang('embed_title'),
        description=lang('embed_description', msg.user.display_name),
        color=Color.white()
    ).set_image(url=f'https://cdn.discordapp.com/attachments/1137786275701727343/{choice(images)}')

    return msg.custom_reply(embed=embed)
