from __future__ import annotations
from json import load
from itertools import chain
from typing import Callable, TYPE_CHECKING

from discord import Embed, Color, InteractionType

from utils import i18n_provider, cooldowns, permission_translator, error_handler, message_component_handler, get_owner_only_folders, autocomplete_generator, better_partial
if TYPE_CHECKING:
  from discord import Interaction
  from main import MyClient
  from utils import Command

with open('config.json', 'r', encoding='utf8') as file:
  config = load(file)

owner_only_folders = get_owner_only_folders()
error_embed = Embed(color=Color.red())

def add_properties(client: MyClient, interaction: Interaction):
  interaction.guild.db = lambda key: client.db.get('GUILD_SETTINGS', interaction.guild.id + (f'.{key}' if key else ''))
  interaction.guild.local_code = lambda _: \
    interaction.guild.db('config.lang') or interaction.guild.preferred_locale[:2] or client.default_settings['config.lang']
  interaction.command_name = interaction.command.name if interaction.command else None

async def interaction_validator(interaction: Interaction, command: Command, lang):
  """returns `True` if everything is fine"""

  if command.disabled:
    if config.get('replyOnDisabledCommand') is False: return None
    error_embed.description = lang('events.command_disabled')
    return await interaction.response.send_message(embed=error_embed)

  if interaction.client.bot_type == 'dev' and not command.beta:
    if config.get('replyOnNonBetaCommand') is False: return None
    error_embed.description = lang('events.command_non_beta')
    return await interaction.response.send_message(embed=error_embed, ephemeral=True)

  disabled_list = interaction.guild.db[f'command_settings.{command.alias_of or command.name}.disabled'] or \
      {'members': [], 'channels': [], 'roles': []}

  if interaction.user.id in disabled_list['members']:
    error_embed.description = lang('events.not_allowed.member')
    return await interaction.response.send_message(embed=error_embed, ephemeral=True)

  if interaction.user.id in disabled_list['channels']:
    error_embed.description = lang('events.not_allowed.channel')
    return await interaction.response.send_message(embed=error_embed, ephemeral=True)

  if disabled_list['roles'] and any(e.id in disabled_list['roles'] for e in interaction.member.roles.cache):
    error_embed.description = lang('events.not_allowed.role')
    return await interaction.response.send_message(embed=error_embed, ephemeral=True)

  if command.category.lower() == 'nsfw' and not interaction.channel.nsfw:
    error_embed.description = lang('events.nsfw_command')
    return await interaction.response.send_message(embed=error_embed, ephemeral=True)

  for option in list(chain.from_iterable(command.options)):
    if option.autocomplete_options and option.strict_autocomplete and interaction.options.get(option.name) and not any(
        interaction.options.get(option.name).value.lower() in (e.lower() if isinstance(e, str) else e['value'].lower())
        for e in autocomplete_generator(interaction, command, lang.__self__.locale) or []
    ):
      error_embed.description = lang('events.strict_autocomplete_no_match')
      return await interaction.response.send_message(embed=error_embed, ephemeral=True)

  if interaction.client.bot_type != 'dev':
    cooldown = cooldowns(interaction, command.name, command.cooldowns)
    if cooldown:
      error_embed.description = lang('events.cooldown', cooldown)
      return await interaction.response.send_message(embed=error_embed, ephemeral=True)

  return True

async def run(client, interaction: Interaction):
  if interaction.user.id in client.settings.blacklist: return None

  locale = interaction.guild.db['config.lang'] or interaction.guild.local_code
  if interaction.type == InteractionType.component:
    return message_component_handler(interaction, better_partial(i18n_provider.__, locale=locale))

  command = client.slash_commands.get(interaction.command_name)

  if command and interaction.type == InteractionType.autocomplete:
    return interaction.response.autocomplete(autocomplete_generator(interaction, command, locale) or [])

  lang = better_partial(
      i18n_provider.__, locale=locale,
      backup_path=f'commands.{command.category.lower()}.{command.alias_of or command.name}' if command else None
  )

  # DO NOT REMOVE THIS STATEMENT!
  if (
      not isinstance(command, Command)
      or (command.category.lower() in owner_only_folders and interaction.user.id != client.application.owner.id)
      or not await interaction_validator(interaction, command, lang)
  ): return None

  if interaction.type == InteractionType.application_command:
    user_perms_missing = [e for e in command.permissions.user if e not in interaction.user.resolved_permissions]
    client_perms_missing = [e for e in command.permissions.user if e not in interaction.guild.me.resolved_permissions]

    if user_perms_missing or client_perms_missing:
      error_embed.title = lang('events.permission_denied.embed_title')
      error_embed.description = lang(
          f"events.permission_denied.embed_description_{'user' if user_perms_missing else 'bot'}",
          permissions='`, `'.join(permission_translator(user_perms_missing or client_perms_missing))
      )

      return await interaction.response.send_message(embed=error_embed, ephemeral=True)

    if not command.no_defer and not interaction.response.is_done(): await interaction.response.defer(ephemeral=command.ephemeral_defer or False)

    try:
      await command.run(interaction, lang)
      if client.bot_type != 'dev':
        client.db.set('BOT_SETTINGS', f'stats.{command.name}', (client.settings[f'stats.{command.name}'] or 1) + 1)
    except Exception as err:  # pylint:disable=broad-exception-caught
      return error_handler(client, err, interaction, lang)
