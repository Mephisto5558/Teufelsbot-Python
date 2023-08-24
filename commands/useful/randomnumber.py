from math import isnan
from random import randint

from utils import Aliases, Command, Option


class RandomNumber(Command):
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

  def run(self, msg, lang):
    min_value = msg.options.getInteger('minimum') or int(msg.args[0]) if msg.args else None
    max_value = msg.options.getInteger('maximum') or int(msg.args[1]) if len(msg.args) > 1 else None

    if min_value is None or isnan(min_value): min_value = 0
    if max_value is None or isnan(max_value): max_value = 100

    try:
      result = randint(min_value, max_value) if min_value < max_value else randint(max_value, min_value)
      msg.customReply(str(result))
    except ValueError as err:
      if str(err) == 'empty range for randrange()':
        msg.customReply(lang('outOfRange', err.args[0]))
      else:
        raise err
