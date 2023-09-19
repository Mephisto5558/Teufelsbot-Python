from discord import Interaction

def fact(interaction:Interaction, lang):
  lang.__boundArgs__[0].backupPath = 'commands.fun.fact'

  interaction.response.edit_message(components=[])

  interaction.client.slash_commands.get('fact').run(interaction, lang)
