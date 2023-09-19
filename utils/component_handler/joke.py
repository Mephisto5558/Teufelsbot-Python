from discord import Interaction

def joke(interaction: Interaction, lang, api: str | None = None, type_: str | None = None, blacklist: str | None = None, max_length: int | None = None):
  lang.__boundArgs__[0].backupPath = 'commands.fun.joke'

  def get_string(value):
    match value:
      case 'api': return None if api == 'None' else api
      case 'type': return None if type_ == 'None' else type_
      case 'blacklist': return None if blacklist == 'None' else blacklist
    return None

  interaction.oprions = {
      'get_string': get_string,
      'get_integer': lambda: None if max_length == 'None' else max_length
  }

  interaction.response.edit_message(components=[])

  interaction.client.slash_commands.get('joke').run(interaction, lang)
