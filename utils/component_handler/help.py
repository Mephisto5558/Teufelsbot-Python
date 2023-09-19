from discord import Interaction

from .help_utils import all_query, category_query, command_query

utils = {'command': command_query, 'category': category_query, 'all': all_query}

async def help_(interaction: Interaction, lang, type_: str):
  lang.__boundArgs__[0].backupPath = 'commands.information.help'

  await interaction.response.edit_message()
  return utils[type_](interaction, lang, interaction.values[0])
