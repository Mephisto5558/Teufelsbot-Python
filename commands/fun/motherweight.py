from random import randint

from utils import Aliases, Command, Option

class CustomCommand(Command):
  name = 'motherweight'
  aliases = Aliases(prefix=['mutterwaage'])
  slash_command = True
  prefix_command = True
  options = [Option(name='target', type='User')]

  async def run(self, msg, lang):
    target = msg.options.get_member('target') or msg.mentions.members.first() or next((e for e in msg.guild.members if any(
        item in [e.user.id, e.user.name, e.user.tag, e.nickname] for item in [*(msg.args or []), msg.content])), None)
    weight = randint(0, 1000)

    return msg.custom_reply(
        content=lang(f"responses_{'others' if target else 'self'}.{weight/100}", user=target.displayName if target else None)
        + lang('weight', weight)
    )
