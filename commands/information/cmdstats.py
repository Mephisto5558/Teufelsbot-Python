from operator import itemgetter

from discord import Embed, Color

from utils import Command, Option, Cooldowns, list_commands, get_owner_only_folders

owner_only_folders = get_owner_only_folders()

class CMD(Command):
  name = 'cmdstats'
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = True
  dm_permission = True
  options = [Option(
      name='command',
      type='String',
      autocomplete_options=lambda i: [e.name for e in list_commands(i)],
      strict_autocomplete=True
  )]

  def run(self, msg, lang):
    command = msg.options.get_string('command') or msg.args[0]
    embed = Embed(title=lang('embed_title'), color=Color.white())

    if command:
      id_ = next(e.id for e in msg.client.application.commands.cache if e.name == command)
      embed.description = lang(
          'embed_description', command=f'</{command}:{id_}>' if id_ else '`/{command}`', count=msg.client.settings[f'stats.{command}'] or 0)
    else:
      commands = [
          (k, v) for k, v in msg.client.settings['stats'].items()
          if (msg.client.prefix_commands.get(k) or msg.client.slash_commands.get(k)).category.lower() not in owner_only_folders
      ]

      embed.description = lang('embed_description_many')
      embed.fields = [{
          'name': f"</{k}:{msg.client.application.commands.cache.get(k).name}>" if msg.client.application.commands.cache.get(k) else f"/{k}",
          'value': f"**{v}**",
          'inline': True
      } for k, v in sorted(commands, key=itemgetter(1), reverse=True)[:10]]

      return msg.custom_reply(embed=embed)
