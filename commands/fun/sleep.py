from discord import Message

from utils import Command

class CMD(Command):
  name = 'sleep'
  slash_command = False
  prefix_command = True
  dm_permission = True

  async def run(self, msg: Message, lang):
    if msg.member.moderatable and msg.member.display_name.length < 26 and not msg.member.nickname.startswith('[AFK] '):
      return msg.member.set_nickname(f'[AFK] {msg.member.display_name}')

    msg.client.db.set(
        'USER_SETTINGS',
        f'{msg.user.id}.afk_message',
        {'message': lang('afk_message'), 'createdAt': str(round(msg.created_at / 1000))}
    )
    return msg.custom_reply(content=lang('response_list', msg.member.custom_name))
