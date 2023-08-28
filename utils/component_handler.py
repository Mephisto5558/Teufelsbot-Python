from .cooldowns import cooldowns
from .component_handler import handlers

def message_component_handler(interaction, lang):
  feature, *args = interaction.custom_id.split('.') + [None]
  cooldown = cooldowns(interaction, f'button_press_event.{interaction.message.id}', {'user': 1000})
  command = interaction.client.slash_commands.get(feature) or interaction.client.prefix_commands.get(feature)
  error_embed = {'color': 'Red', 'set_description': lambda: None}
  disabled_list = interaction.guild.db[f'commandSettings.{command.alias_of or command.name}.disabled'] or {}

  member_list: list = disabled_list.get('members', [])
  channel_list: list = disabled_list.get('channels', [])
  role_list: list = disabled_list.get('roles', [])

  if interaction.user.id in member_list:
    return interaction.reply(embeds=[error_embed.set_description(lang('events.notAllowed.member'))], ephemeral=True)
  if interaction.channel.id in channel_list:
    return interaction.reply(embeds=[error_embed.set_description(lang('events.notAllowed.channel'))], ephemeral=True)
  if any(role.id in role_list for role in interaction.member.roles):
    return interaction.reply(embeds=[error_embed.set_description(lang('events.notAllowed.role'))], ephemeral=True)
  if command.category.lower() == 'nsfw' and not interaction.channel.nsfw:
    return interaction.reply(embeds=[error_embed.set_description(lang('events.nsfwCommand'))], ephemeral=True)
  if cooldown:
    return interaction.reply(content=lang('events.buttonPressOnCooldown', cooldown), ephemeral=True)

  if handlers[feature] and hasattr(handlers[feature], 'main') and callable(handlers[feature].main):
    return handlers[feature].main(interaction, lang, *args)
