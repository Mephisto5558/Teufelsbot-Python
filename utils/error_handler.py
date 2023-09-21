from __future__ import annotations
from json import load, dumps
from typing import Callable, TYPE_CHECKING
from io import BytesIO

from requests import HTTPError, post
from discord import DiscordException, File, ButtonStyle, Button, ActionRow, Color, Embed, Message, Interaction

from .logger import log
if TYPE_CHECKING:
  from main import MyClient

with open('config.json', 'r', encoding='utf8') as file:
  config = load(file)

async def error_handler(client: MyClient, error: Exception, message: Message | Interaction, lang: Callable):
  log.error(' [ERROR HANDLING] :: Uncaught Error\n%s', error.args[0].stack)

  if not message: return None

  lang.__self__.backup_path = 'events.error_handler'

  command = client.slash_commands.get(message.command_name) or client.prefix_commands.get(message.command_name)
  if command.alias_of: command = client.slash_commands.get(command.alias_of) or client.prefix_commands.get(command.alias_of)

  embed = Embed(
      title=lang('embed_title'),
      description=lang('embed_description', command=command.name if command else message.command_name),
      color=Color.dark_red()
  ).set_footer(text=lang('embed_footer_text'))
  component = ActionRow(Button(
      custom_id='error_handler.report_error',
      label=lang('report_button') + (lang('report_button_disabled') if client.bot_type == 'dev' else ''),
      style=ButtonStyle.danger,
      disabled=client.bot_type == 'dev'
  ))

  msg = await message.custom_reply(embed=embed, components=[component])

  if client.bot_type == 'dev':
    return None

  @msg.on_component_collect
  async def collector(client: MyClient, component: Interaction):
    await component.response.defer()

    try:
      github = config.get('GitHub')

      if github and client.keys.github_key:
        res = await post(
            f"https://api.github.com/repos/{github.get('UserName')}/{github.get('RepoName')}/issues",
            headers={
                'Authorization': f'Token {client.keys.github_key}',
                'User-Agent': f"Bot {github.get('Repo')}"
            },
            data=dumps({
                'title': f'{error.args[0].name}: {error.args[0].message} in command "{message.command_name}"',
                'body': f'<h3>Reported by {component.user.name} ({component.user.id}) with bot {client.user.id}</h3>\n\n{error.args[0].stack}',
                'labels': ['bug']
            }),
            timeout=10
        )
        json = res.json()

        if not res.ok: raise HTTPError(res, json)

        message_json = dumps(message, default=lambda v: str(v) if isinstance(v, int) else v, indent=2)
        try: client.application.owner.send(content=json.html_url, file=File(BytesIO(message_json.encode(encoding='utf8')), filename='data.json'))
        except DiscordException: pass

        embed.footer = None
        embed.description = lang('report_success', json.html_url)
        return msg.edit(embeds=embed, components=[])
    except (DiscordException, HTTPError) as err:
      log.error(err.args[0].stack)
      return message.custom_reply(lang('report_fail', err.args[0].message or 'unknown error'))

  @collector.on_end
  def on_end(collected):
    if not collected: return None

    component.children[0].disabled = True
    return msg.edit(embed=embed, component=component)
