def reddit(interaction, lang, subreddit, type_, filter_nsfw):
  lang.__boundArgs__[0].backupPath = 'commands.fun.reddit'

  interaction.options = {
      'get_boolean': lambda: filter_nsfw == 'True',
      'get_string': lambda str_: type_ if str_ == 'type' else subreddit
  }

  interaction.update(components=[])

  interaction.client.slash_commands.get('reddit').main(interaction, lang)
