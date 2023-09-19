from requests import get

from discord import ButtonStyle, Button, ActionRow, Embed, Color

from utils import Command, Cooldowns

class CMD(Command):
  name = 'fact'
  cooldowns = Cooldowns(guild=100)
  slash_command = True
  prefix_command = True
  dm_permission = True

  async def run(self, msg, lang):
    data = get(f'https://uselessfacts.jsph.pl/api/v2/facts/random?language={lang}', timeout=10).json()

    embed = Embed(
        title=lang('embed_title'),
        description=f'{data.text}\n\nSource: [{data.source}]({data.source_url})',
        color=Color.random()
    ).set_footer(text='- https://uselessfacts.jsph.pl')

    component = ActionRow([Button(label=lang('global.anotherone'), custom_id='fact', style=ButtonStyle.primary)])

    return msg.custom_reply(embed=embed, components=[component])
