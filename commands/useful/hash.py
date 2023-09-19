import hashlib

from discord import Interaction, Embed, Color

from utils import Command, Option, Cooldowns

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

  async def run(self, msg: Interaction, lang):
    input_: str = msg.options.get_string('input')
    method = msg.options.get_string('method')
    embed = Embed(
        title=lang('embed_title'),
        description=lang('embed_description', input=input_[:500] + '...' if len(input_) > 500 else input_, method=method),
        color=Color.dark_gold()
    )

    hash_ = hashlib.new(method, data=input_.encode()).hexdigest()
    return msg.response.edit_message(content=lang('text', hash_), embed=embed)
