def topic(interaction, lang):
  lang.__boundArgs__[0].backupPath = 'commands.fun.topic'

  interaction.update(components=[])

  interaction.client.slash_commands.get('topic').main(interaction, lang)