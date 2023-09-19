from .i18n_provider import i18n_provider
from .command_class import Command

def autocomplete_generator(msg, command: Command, locale: str):
  if not command.options: return None

  # pylint: disable=protected-access
  def response(v: str):
    return {
        'name': i18n_provider.__(
            key=f"commands.{command.category.lower()}.{command.name}.options.{msg.options._group + '.' if msg.options._group else ''}{msg.options._subcommand + '.' if msg.options._subcommand else ''}{msg.focused.name}.choices.{v}",
            locale=locale, none_not_found=True
        ) or v,
        'value': v
    }

  options = command.options
  if msg.options._group:
    options = next((e for e in options if e.name == msg.options._group), [])
  if msg.options._subcommand:
    options = next((e for e in options if e.name == msg.options._subcommand), {}).get('options', [])
  options = next((e for e in options if e.name == msg.focused.name), {}).get('autocompleteOptions', [])

  if callable(options): options = options()
  if isinstance(options, dict): return [options[:25]]
  if isinstance(options, str): return [response(options)]
  return [response(e) for e in options[:25] if msg.focused.value.lower() in (e if isinstance(e, str) else e.value).lower()]
