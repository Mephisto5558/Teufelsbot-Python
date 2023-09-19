from importlib import import_module
from os import listdir
from os.path import splitext

from discord import InteractionType, Embed, Color, Interaction

from .cooldowns import cooldowns

handlers = [
    import_module('utils.component_handler.' + splitext(file)[0]).__dict__[splitext(file)[0]]
    for file in listdir('utils/component_handler')
    if file.endswith('.py')
]

async def message_component_handler(interaction: Interaction, lang):
  feature, *args = interaction.custom_id.split('.') + [None]
  cooldown = cooldowns(interaction, f'button_press_event.{interaction.message.id}', {'user': 1000})
  command = interaction.client.slash_commands.get(feature) or interaction.client.prefix_commands.get(feature)
  error_embed = Embed(color=Color.red())
  disabled_list = interaction.guild.db[f'command_settings.{command.alias_of or command.name}.disabled'] or {}

  member_list: list = disabled_list.get('members', [])
  channel_list: list = disabled_list.get('channels', [])
  role_list: list = disabled_list.get('roles', [])

  if interaction.user.id in member_list:
    error_embed.description = lang('events.not_allowed.member')
    await interaction.response.send_message(embeds=[error_embed], ephemeral=True)
  elif interaction.channel.id in channel_list:
    error_embed.description = lang('events.not_allowed.channel')
    await interaction.response.send_message(embeds=[], ephemeral=True)
  elif any(role.id in role_list for role in interaction.user.roles):
    error_embed.description = lang('events.not_allowed.role')
    await interaction.response.send_message(embeds=[], ephemeral=True)
  elif command.category.lower() == 'nsfw' and not interaction.channel.nsfw:
    error_embed.description = lang('events.nsfw_command')
    await interaction.response.send_message(embeds=[], ephemeral=True)
  elif cooldown:
    await interaction.response.send_message(content=lang('events.button_press_on_cooldown', cooldown), ephemeral=True)
  elif handlers[feature] and callable(handlers[feature]):
    handlers[feature](interaction, lang, *args)
