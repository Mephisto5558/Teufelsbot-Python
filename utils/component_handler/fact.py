def fact(interaction, lang):
  lang.__boundArgs__[0].backupPath = 'commands.fun.fact'
  
  interaction.update(components=[])

  interaction.client.slash_commands.get('fact').run(interaction, lang)