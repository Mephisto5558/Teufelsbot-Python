from discord import Message

from utils import Command, log

class CMD(Command):
  name = 'eval'
  slash_command = False
  prefix_command = True
  dm_permission = True
  beta = True

  async def run(self, msg: Message, lang):
    # pylint:disable=eval-used, broad-exception-caught
    if not msg.content: return None

    try:
      eval(msg.content)
      await msg.reply(lang('success', lang('finished', msg.content)))
    except Exception as err:
      await msg.reply(lang('error', msg=lang('finished', msg.content), name=str(err), err=err.args[0]))

    return log.debug("evaluated command '%s'", msg.content)
