from secrets import choice
from discord import Interaction

from utils import Command, Cooldowns, Option

default_charset = ['abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?§$%&/\\=*\'"#*(){}[]']

class CMD(Command):
  name = 'passwordgenerator'
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = False
  dm_permission = True
  ephemeral_defer = True
  options = [
      Option(name='length', type='Integer', max_value=1750),
      Option(name='count', type='Integer', max_value=500),
      Option(name='exclude_chars', type='String'),
      Option(name='include_chars', type='String')
  ]

  async def run(self, msg: Interaction, lang):
    count = msg.options.get_integer('count') or 1
    length = msg.options.get_integer('length') or 12
    exclude = msg.options.get_string('exclude_chars') or ''
    include = msg.options.get_string('include_chars') or ''
    password_list = []

    charset = ''.join([char for char in default_charset + list(include) if char not in exclude])
    if not charset: return msg.response.edit_message(content=lang('charset_empty'))

    for _ in range(count):
      last_random_char = ''
      if (len(password_list) + length) > 1743:
        break

      random_chars = []
      for _ in range(length):
        random_char = choice(charset.strip(last_random_char))
        # Todo: check if necessary to implement:
        # https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Useful/passwordgenerator.js#L47-L50
        random_chars.append(random_char)
      password_list.append(''.join(random_chars))

    if len(charset) > 100: charset = charset[:97] + '...'

    return msg.response.edit_message(content=lang('success', passwords=password_list, charset=charset))
