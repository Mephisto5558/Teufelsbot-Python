from utils import Command

class CMD(Command):
  name = 'sleep'
  slash_command = False
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    if msg.member.moderatable and msg.member.display_name.length < 26 and not msg.member.nickname.startswith('[AFK] '):
      return msg.member.set_nickname(f'[AFK] {msg.member.display_name}')

    msg.client.db.set('USERSETTINGS', f'{msg.user.id}.afk_message', {'message': lang('afk_message'), 'createdAt': str(round(msg.created_timestamp/1000))})
    return msg.custom_reply(lang('response_list', msg.member.custom_name))