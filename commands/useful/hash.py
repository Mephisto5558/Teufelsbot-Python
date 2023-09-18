import hashlib

from utils import Command, Option, Cooldowns, Colors

class CMD(Command):
  name = 'hash'
  cooldowns = Cooldowns(user=1e4)
  slash_command = True
  prefix_command = False
  dm_permission = True
  ephemeral_defer = True
  options = [
      Option(name='input', type='String', required=True),
      Option(name='method', type='String', autocomplete_options=hashlib.algorithms_guaranteed, strict_autocomplete=True)
  ]

  def run(self, msg, lang):
    input_: str = msg.options.get_string('input')
    method = msg.options.get_string('method')
    embed = EmbedBuilder(
        title=lang('embed_title'),
        description=lang('embed_description', input=input_[:500] + '...' if len(input_) > 500 else input_, method=method),
        color=Colors.DarkGold
    )

    hash_ = hashlib.new(method, data=input_.encode()).hexdigest()
    return msg.edit_reply(content=lang('text', hash_), embeds=[embed])
