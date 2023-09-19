from discord import Interaction

def topic(interaction:Interaction, lang):
  lang.__boundArgs__[0].backupPath = 'commands.fun.topic'

  interaction.response.edit_message(components=[])

  interaction.client.slash_commands.get('topic').main(interaction, lang)