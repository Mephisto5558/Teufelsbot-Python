from utils import Command, Option, list_commands
from utils.component_handler import all_query, command_query, category_query

class CMD(Command):
  name = 'help'
  slash_command = True
  prefix_command = True
  dm_permission = True
  ephemeral_defer = True
  beta = True
  options = [
      Option(
          name='category',
          type='String',
          autocomplete_options=lambda i: {e.category for e in list_commands(i)},
          strict_autocomplete=True
      ),
      Option(
          name='command',
          type='String',
          autocomplete_options=lambda i: {e.name for e in list_commands(i)},
          strict_autocomplete=True
      )
  ]

  def run(self, msg, lang):
    cat_query = msg.options.get_string('category')
    cmd_query = msg.options.get_string('command') or msg.args[0].lower() if msg.args else None

    if cmd_query: return command_query(msg, lang, cmd_query)
    if cat_query: return category_query(msg, lang, cat_query)
    return all_query(msg, lang)
