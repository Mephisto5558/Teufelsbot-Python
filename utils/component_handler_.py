from importlib import import_module
from os import listdir
from os.path import splitext

from .cooldowns import cooldowns

handlers = [import_module('utils.component_handler.' + splitext(file)[0]).__dict__[splitext(file)[0]] for file in listdir('utils/component_handler') if file.endswith('.py')]

def message_component_handler(interaction, lang):
  feature, *args = interaction.custom_id.split('.') + [None]
  cooldown = cooldowns(interaction, f'button_press_event.{interaction.message.id}', {'user': 1000})
  command = interaction.client.slash_commands.get(feature) or interaction.client.prefix_commands.get(feature)
  error_embed = {'color': 'Red'}
  disabled_list = interaction.guild.db[f'command_settings.{command.alias_of or command.name}.disabled'] or {}

  member_list: list = disabled_list.get('members', [])
  channel_list: list = disabled_list.get('channels', [])
  role_list: list = disabled_list.get('roles', [])

  if interaction.user.id in member_list:
    interaction.reply(embeds=[error_embed.set_description(lang('events.not_allowed.member'))], ephemeral=True)
  elif interaction.channel.id in channel_list:
    interaction.reply(embeds=[error_embed.set_description(lang('events.not_allowed.channel'))], ephemeral=True)
  elif any(role.id in role_list for role in interaction.member.roles):
    interaction.reply(embeds=[error_embed.set_description(lang('events.not_allowed.role'))], ephemeral=True)
  elif command.category.lower() == 'nsfw' and not interaction.channel.nsfw:
    interaction.reply(embeds=[error_embed.set_description(lang('events.nsfw_command'))], ephemeral=True)
  elif cooldown:
    interaction.reply(content=lang('events.button_press_on_cooldown', cooldown), ephemeral=True)
  elif handlers[feature] and callable(handlers[feature]):
    handlers[feature](interaction, lang, *args)
