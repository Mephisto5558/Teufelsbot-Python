from datetime import datetime
from hashlib import sha256
from os import getcwd
from random import choice, seed

from utils import Command, Aliases, Option

class CMD(Command):
  name = '8ball'
  aliases = Aliases(prefix=['eightball'])
  slash_command = True
  prefix_command = True
  dm_permission = True
  options = [Option(name='question', type='String', required=True)]

  async def run(self, msg, lang):
    input_str = msg.options.get_string('question') or msg.content
    if not input_str: return msg.custom_reply(lang('no_question'))

    now = datetime.now()
    seed_str = f'{input_str.lower()}_{getcwd()}_{now.year}-{now.month}-{now.day}'

    seed(int(sha256(seed_str.encode()).hexdigest(), 16))

    response_list = lang.__self__.locale_data[f"{lang.keywords['locale']}.{lang.keywords['backup_path']}.response_list"]
    return msg.custom_reply(content=choice(response_list))
