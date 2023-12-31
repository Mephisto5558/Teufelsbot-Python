from __future__ import annotations
from functools import partial
from typing import TYPE_CHECKING

from discord import Embed, ComponentType, Interaction, Color, ActionRow, SelectMenu


from ..i18n_provider import I18nProvider
from ..command_class import Command
from ..permission_translator import permission_translator
from ..get_owner_only_folders import get_owner_only_folders

if TYPE_CHECKING:
  from main import MyClient
owner_only_folders = get_owner_only_folders()

def get_all_commands(interaction: Interaction) -> list[Command]:
  unique_commands = list(set(list(interaction.client.prefix_commands.values()) + list(interaction.client.slash_commands.values())))
  return list(filter(partial(filter_commands, interaction=interaction), unique_commands))

def create_category_component(interaction: Interaction, lang, command_categories: list | set | None = None):
  if not command_categories:
    command_categories = {e.category for e in [*interaction.client.prefix_commands.values(), *interaction.client.slash_commands.values()]}

  if interaction.user.id != interaction.client.application.owner.id:
    command_categories = {e for e in command_categories if e.lower() not in owner_only_folders}

  default_option = (
      ((interaction.options.get_string('command') or interaction.options.get_string('category')) if interaction.options else None)
      or (
          interaction.client.prefix_commands.get(interaction.args[0])
          or interaction.client.slash_commands.get(interaction.args[0]) if interaction.args else None
      )
      or (next(
          (e for e in interaction.message.components[0].components[0].options if e.value == interaction.values[0]), None
      ) if interaction.values else None)
  )

  if interaction.message and interaction.message.components:
    if default_option:
      for i, option in enumerate(interaction.message.components[0].components[0].options):
        if option.default and option.value == interaction.values[0]:
          del interaction.message.components[0].components[0].options[i]
          break
      default_option.default = True
    return interaction.message.components[0]

  return ActionRow(components=[SelectMenu(
      custom_id='help.category',
      type=ComponentType.select,
      placeholder=lang('categoryListPlaceholder'),
      min_values=0,
      options=[{
          'label': lang(f'options.category.choices.{e.lower()}'),
          'value': e.lower(),
          'default': default_option and default_option.value == e
      } for e in command_categories]
  )]
  )

def create_commands_component(interaction: Interaction, lang, category: str):
  default_option = (
      (interaction.args[0] if interaction.args else None) or (
          interaction.options.get_string('command') if interaction.options else None) or (
          next(
              (e for e in interaction.message.components[1].components[0].options if e.value == interaction.values[0]),
              None) if interaction.message and interaction.message.components[1] else None))

  return ActionRow({
      'components': [SelectMenu({
          'type': ComponentType.select,
          'customId': 'help.command',
          'placeholder': lang('commandListPlaceholder'),
          'min_values': 0,
          'options': [
              {'label': e.name, 'value': e.name, 'default': default_option and default_option.value == e.name}
              for e in get_all_commands(interaction)
              if e.category.lower() == category and not e.alias_of
          ]
      })]
  })

def create_info_fields(interaction: Interaction, cmd: Command, lang, help_lang):
  if not cmd: return []
  arr = []
  prefix = interaction.guild.db['config.prefix'] or interaction.client.default_settings['config.prefix']

  if cmd.aliases.prefix:
    arr.append({'name': lang('one.prefixAlias'), 'value': f"`{'`, `'.join(cmd.aliases.prefix)}`", 'inline': True})

  if cmd.aliases.slash:
    arr.append({'name': lang('one.slashAlias'), 'value': f"`{'`, `'.join(cmd.aliases.slash)}`", 'inline': True})

  if cmd.alias_of:
    arr.append({'name': lang('one.aliasOf'), 'value': f'`{cmd.alias_of}`', 'inline': True})

  if cmd.permissions.client: arr.append({
      'name': lang('one.botPerms'),
      'value': f"`{'`, `'.join(permission_translator(cmd.permissions.client, lang.__boundArgs__[0]['locale']))}`",
      'inline': False
  })

  if cmd.permissions.user: arr.append({
      'name': lang('one.userPerms'),
      'value': f"`{'`, `'.join(permission_translator(cmd.permissions.user, lang.__boundArgs__[0]['locale']))}`",
      'inline': True
  })

  if cmd.cooldowns.user or cmd.cooldowns.guild:
    cooldowns = []
    for k, v in cmd.cooldowns.items():
      if v:
        min_ = v // 60000  # int divide
        sec = (v % 60000) / 1000
        sec = sec if sec % 1 == 0 else round(sec, 2)

        if min_ and sec:
          cooldowns.append(f"{lang('global.' + k)}: {min_}min {sec}s")
        else:
          cooldowns.append(f"{lang('global.' + k)}: {min_}min" if min_ else f"{lang('global.' + k)}: {sec}s")

    arr.append({'name': lang('one.cooldowns'), 'inline': False, 'value': ', '.join(cooldowns)})

  if help_lang('usage.usage'):
    arr.append({'name': '```' + lang('one.usage') + '```', 'value': help_lang('usage.usage', prefix), 'inline': True})
    arr.append({'name': '```' + lang('one.examples') + '```', 'value': help_lang('usage.examples', prefix), 'inline': True})

  return arr

def filter_commands(cmd: Command, interaction: Interaction | None = None, client: MyClient | None = None):
  """`client` is only required if interaction is None"""

  if not interaction:
    if not client: return False
    interaction = {'client': client}
  return (
      cmd and cmd.name and not cmd.disabled,
      interaction['client'].bot_type != 'dev' or cmd.beta or (
          cmd.category.lower() in owner_only_folders
          and ('user' in interaction and interaction.user.id != interaction.client.application.owner.id)
      )
  )

def all_query(interaction, lang):
  command_categories = {e.category for e in get_all_commands(interaction)}
  if interaction.user.id != interaction.client.application.id:
    command_categories = {e for e in command_categories if e.lower() not in owner_only_folders}

  embed = Embed(
      title=lang('all.embed_title'),
      description=lang('all.embed_description' if command_categories else 'all.not_found'),
      color=Color.blurple() if command_categories else Color.red()
  ).set_footer(text=lang('all.embed_footer_text'))

  for category in command_categories: embed.add_field(
      name=lang(f'options.category.choices.{category.lower()}'),
      # U+200E (LEFT-TO-RIGHT MARK) is used to make a newline for better spacing
      value=lang(f'commands.{category.lower()}.category_description') + '\n‎',
      inline=True
  )

  return interaction.custom_reply(embeds=[embed], components=[create_category_component(interaction, lang, command_categories)])

def category_query(interaction: Interaction, lang, query: str):
  if not query:
    for i, option in enumerate(interaction.message.components[0].components[0].options):
      if option.default: del interaction.message.components[0].components[0].options[i]
    return all_query(interaction, lang)

  help_lang = partial(I18nProvider.__, none_not_found=True, locale=interaction.guild.locale_code, backup_path=f'commands.{query}')
  commands = get_all_commands(interaction)
  embed = Embed(title=lang(f'options.category.choices{query}'), color=Color.blurple())

  for command in commands:
    if command.category.lower() == query and not command.alias_of and filter_commands(command, interaction):
      embed.add_field(name=command.name, value=help_lang(key=f'{command.name}.description') + '\n‎', inline=True)

  if not embed.fields: embed.description = lang('all.notFound')

  return interaction.custom_reply(embeds=[embed], components=[
      create_category_component(interaction, lang),
      create_commands_component(interaction, lang, query)
  ])

def command_query(interaction, lang, query: str):
  if len(interaction.values) == 0: return category_query(interaction, lang, [e.value for e in interaction.message.components[0].components[0].data.options if e.default][0])

  command: Command = interaction.client.slash_commands.get(query) or interaction.client.prefix_commands.get(query)
  if not filter_commands(command, interaction):
    embed = Embed(description=lang('one.notFound', query), color=Color.red())

    return interaction.custom_reply(embeds=[embed], components=[create_category_component(interaction, lang)])

  help_lang = partial(
      I18nProvider.__, none_not_found=True, locale=interaction.guild.locale_code,
      backup_path=f'commands.{command.category.lower()}.{command.name}'
  )

  embed = Embed(
      title=lang('one.embed_title', category=command.category, command=command.name),
      description=help_lang(key='description'),
      color=Color.blurple(),
  ).set_footer(
      text=lang('one.embed_footer_text', interaction.guild.db['config.prefix'] or interaction.client.default_settings['config.prefix'])
  )

  embed.fields = create_info_fields(interaction, command, lang, help_lang),

  return interaction.customReply(embeds=[embed], components=[
      create_category_component(interaction, lang), create_commands_component(interaction, lang, command.category.lower())
  ])
