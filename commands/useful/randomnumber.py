from math import isnan

from utils import Aliases, Command, Option, random_int


class CMD(Command):
  name = 'randomnumber'
  aliases = Aliases(prefix=['random-number'])
  slashCommand = True
  prefixCommand = True
  dmPermission = True
  ephemeralDefer = True
  options = [
      Option(name='minimum', type='Integer'),
      Option(name='maximum', type='Integer')
  ]

  async def run(self, msg, lang):
    min_value = msg.options.get_integer('minimum') or int(msg.args[0]) if msg.args else None
    max_value = msg.options.get_integer('maximum') or int(msg.args[1]) if len(msg.args) > 1 else None

    if min_value is None or isnan(min_value): min_value = 0
    if max_value is None or isnan(max_value): max_value = 100

    try:
      result = random_int(max_value, min_value)
      msg.custom_reply(str(result))
    except ValueError as err:
      msg.custom_reply(lang('out_of_range', err.args[0]))
