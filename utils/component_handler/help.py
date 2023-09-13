from .help_utils import all_query, category_query, command_query

utils = {'command': command_query, 'category': category_query, 'all': all_query}

def help_(interaction, lang, type_: str):
  lang.__boundArgs__[0].backupPath = 'commands.information.help'

  interaction.update()
  return utils[type_](interaction, lang, interaction.values[0])
