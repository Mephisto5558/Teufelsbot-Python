def joke(interaction, lang, api, type_, blacklist, max_length):
  lang.__boundArgs__[0].backupPath = 'commands.fun.joke'

  def get_string(value):
    match value:
      case 'api': return None if api == 'None' else api
      case 'type': return None if type_ == 'None' else type_
      case 'blacklist': return None if blacklist == 'None' else blacklist
    return None

  interaction.options = {
      'get_string': get_string,
      'get_integer': lambda: None if max_length == 'None' else max_length
  }

  interaction.update(components=[])

  interaction.client.slash_commands.get('joke').run(interaction, lang)
