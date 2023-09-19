from discord import Interaction

def reddit(interaction:Interaction, lang, subreddit:str|None=None, type_:str|None=None, filter_nsfw:str|None=None):
  lang.__boundArgs__[0].backupPath = 'commands.fun.reddit'

  interaction.options = {
      'get_boolean': lambda: filter_nsfw == 'True',
      'get_string': lambda str_: type_ if str_ == 'type' else subreddit
  }

  interaction.response.edit_message(components=[])

  interaction.client.slash_commands.get('reddit').main(interaction, lang)
