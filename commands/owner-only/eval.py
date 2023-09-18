from utils import Command, log

class CMD(Command):
  name = 'eval'
  slash_command = False
  prefix_command = True
  dm_permission = True
  beta = True

  def run(self, msg, lang):
    if not msg.content: return None

    try:
      eval(msg.content)
      msg.reply(lang('success', lang('finished', msg.content)))
    except Exception as err:
      msg.reply(lang('error', msg=lang('finished', msg.content), name=str(err), err=err.args[0]))

      return log.debug("evaluated command '%s'", msg.content)
