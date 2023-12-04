from utils import Command, Option, Cooldowns

class CMD(Command):
  name = 'afk'
  cooldowns = Cooldowns(user=5000)
  slash_command = True
  prefix_command = True
  dm_permission = True
  options = [
      Option(name='message', type='String', max_length=1000),
      Option(name='global', type='Boolean')
  ]

  async def run(self, msg, lang):
    global_flag = not msg.guild or msg.options.get_boolean('global') or msg.args[0] == 'global' if msg.args else False
    message = msg.options.get_string('message') or msg.content[7 if global_flag else 0:1000]
    created_at = round(msg.created_at / 1000)

    if global_flag: msg.client.db.set('USER_SETTINGS', f'{msg.user.id}.afk_message', message=message, created_at=created_at)
    else: msg.client.db.set('GUILD_SETTINGS', f'{msg.guild.id}.afk_messages.{msg.user.id}', message=message, created_at=created_at)

    if msg.author and msg.author.moderatable and len(msg.author.display_name) < 26 and (not msg.author.nick or msg.author.nick.startswith('[AFK] ')):
      msg.author.set_nickname(f'[AFK]: {msg.author.display_name}')

    return msg.custom_reply(content=lang('global_success' if global_flag else 'success', message))
