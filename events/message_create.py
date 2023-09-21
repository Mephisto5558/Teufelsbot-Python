from __future__ import annotations
from json import load
from itertools import chain
from typing import Callable, TYPE_CHECKING

from discord import MessageType, ChannelType, Message, Embed, Color

from utils import i18n_provider, cooldowns, permission_translator, error_handler, run_messages, get_owner_only_folders, autocomplete_generator, better_partial
if TYPE_CHECKING:
  from main import MyClient
  from utils import Command, Option

with open('config.json', 'r', encoding='utf8') as file:
  config = load(file)

owner_only_folders = get_owner_only_folders()
error_embed = Embed(color=Color.red())

def add_properties(client: MyClient, message: Message):
  message.guild.db = lambda key: client.db.get('GUILD_SETTINGS', message.guild.id + (f'.{key}' if key else ''))
  message.guild.local_code = lambda _: \
      message.guild.db('config.lang') or message.guild.preferred_locale[:2] or client.default_settings['config.lang']

  prefix_type = 'beta_bot_prefix' if client.bot_type == 'dev' else 'prefix'
  data = message.guild.db(f'config.{prefix_type}') or {}
  case_insensitive: bool | None = data.get('caseinsensitive')
  prefix: str | None = data.get('prefix')

  if not prefix: prefix = client.default_settings[f'config.{prefix_type}']
  if case_insensitive: prefix = prefix.lower()

  if (message.content.lower() if case_insensitive else message.content).startswith(prefix): prefix_length = prefix.length
  elif message.content.startswith(message.user.mention): prefix_length = len(message.user.mention)
  else: prefix_length = 0

  message.user = message.author
  message.original_content = message.content
  message.args: list[str] = message.content[prefix_length:].strip().split(' ')
  message.command_name: str | None = message.args.pop(0).lower() if prefix_length else None
  message.content: str = ' '.join(message.args)

async def message_validator(client: MyClient, message: Message, command: Command, lang: Callable[..., str]):
  """returns `True` if everything is fine"""

  if command.disabled:
    if config.get('replyOnDisabledCommand') is False: return None
    error_embed.description = lang('events.command_disabled')
    await message.reply(embed=error_embed, delete_after=1e4)
    return None

  if command.category.lower() in owner_only_folders and message.user.id != client.application.owner.id:
    return None

  if client.bot_type == 'dev' and not command.beta:
    if config.get('replyOnNonBetaCommand') is False: return None
    error_embed.description = lang('events.command_non_beta')
    await message.reply(embed=error_embed)
    return None

  disabled_list = message.guild.db(f'command_settings.{command.alias_of or command.name}.disabled')
  if isinstance(disabled_list, dict):
    if message.user.id in disabled_list['members']:
      error_embed.description = lang('events.not_allowed.member')
      await message.reply(embed=error_embed, delete_after=1e4)
      return None

    if message.user.id in disabled_list['channels']:
      error_embed.description = lang('events.not_allowed.channel')
      await message.reply(embed=error_embed, delete_after=1e4)
      return None

    if disabled_list['roles'] and any(e in disabled_list['roles'] for e in message.user.roles):
      error_embed.description = lang('events.not_allowed.role')
      await message.reply(embed=error_embed, delete_after=1e4)
      return None

  if command.category.lower() == 'nsfw' and not message.channel.nsfw:
    error_embed.description = lang('events.nsfw_command')
    await message.reply(embed=error_embed, delete_after=1e4)
    return None

  for i, option in enumerate(list(chain.from_iterable(command.options))):
    option: Option

    message.focused = {'name': option.name, 'value': message.args[i]}
    if option.autocomplete_options and option.strict_autocomplete and message.args[i] and not any(
        message.args[i].lower() in (e.lower() if isinstance(e, str) else e['value'].lower())
        for e in autocomplete_generator(message, command, lang.__self__.locale) or []
    ):
      error_embed.description = lang('events.strict_autocomplete_no_match')
      await message.reply(embed=error_embed, delete_after=1e4)
      return None
    del message.focused

  if message.client.bot_type != 'dev':
    cooldown = cooldowns(message, command.name, command.cooldowns)
    if cooldown:
      error_embed.description = lang('events.cooldown', cooldown)
      await message.reply(embed=error_embed, delete_after=1e4)
      return None

  return True

def save_last_mention(client: MyClient, message: Message):
  mentions = {e for e in [
      message.reference.resolved.author.id
      if message.reference and message.reference.resolved and isinstance(message.reference.resolved, Message)
      else None,
      *[u.id for u in message.mentions],
      *[m.id for r in message.role_mentions for m in r.members]
  ] if e and (not client.user or e != client.user.id)}

  if mentions: client.db.set(
      'GUILD_SETTINGS',
      f'{message.guild.id}.last_mentions',
      (message.guild.db('last_mentions') or {}).update({e: {
          'content': message.content,
          'url': message.jump_url,
          'author': message.user.id,
          'channel': message.channel.id,
          'createdAt': message.created_at
      } for e in mentions})
  )

async def run(client: MyClient, message: Message):
  if message.author.id in client.settings.blacklist: return None

  add_properties(client, message)

  config = message.guild.db('config') or {}

  if (all([
      config['autopublish'],
      message.channel.type == ChannelType.news,
      message.type == MessageType.default,
      not message.flags.crossposted,
      message.guild.me.resolved_permissions.read_messages,
      message.guild.me.resolved_permissions.send_messages,
      message.guild.me.resolved_permissions.manage_messages
  ])):
    await message.publish()

  if client.bot_type != 'dev' and message.guild: save_last_mention(client, message)

  if message.user.bot: return None
  if not message.command_name: return run_messages() if message.guild else None

  command = client.slash_commands.get(message)
  lang = better_partial(
      i18n_provider.__, locale=config['lang'] or message.guild.local_code,
      backup_path=f'commands.{command.category.lower()}.{command.alias_of or command.name}' if command else None
  )

  if not command:
    cmd = client.slash_commands.get(message.command_name)
    if not cmd: return run_messages()
    error_embed.description = lang('events.slash_command_only', name=message.command_name, id=cmd.id)
    return message.reply(embed=error_embed, delete_after=1e4)
  elif not await message_validator(client, message, command, lang):
    return run_messages()

  if message.guild:
    user_perms_missing = [e for e in command.permissions.user if e not in message.user.resolved_permissions]
    client_perms_missing = [e for e in command.permissions.user if e not in message.guild.me.resolved_permissions]

    if user_perms_missing or client_perms_missing:
      error_embed.title = lang('events.permission_denied.embed_title')
      error_embed.description = lang(
          f"events.permission_denied.embed_description_{'user' if user_perms_missing else 'bot'}",
          permissions='`, `'.join(permission_translator(user_perms_missing or client_perms_missing))
      )

    return await message.reply(embed=error_embed)

  try:
    await command.run(message, lang)
    if client.bot_type != 'dev':
      client.db.set('BOT_SETTINGS', f'stats.{command.name}', (client.settings[f'stats.{command.name}'] or 1) + 1)
  except Exception as err:  # pylint:disable=broad-exception-caught
    return error_handler(client, err, message, lang)
