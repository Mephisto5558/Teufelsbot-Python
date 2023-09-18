from .i18n_provider import i18n_provider


def autocomplete_generator(msg, command, locale: str):
  if 'options' not in command: return None
  # pylint: disable=protected-access

  def response(v: str):
    return {
        'name': i18n_provider.__(
            key=f"commands.{command.category.lower()}.{command.name}.options.{msg.options._group + '.' if msg.options._group else ''}{msg.options._subcommand + '.' if msg.options._subcommand else ''}{msg.focused.name}.choices.{v}",
            locale=locale, none_not_found=True
        ) or v,
        'value': v
    }

  options: list = command.options
  if msg.options._group:
    options = next((e for e in options if e.name == msg.options._group), [])
  if msg.options._subcommand:
    options = next((e for e in options if e.name == msg.options._subcommand), {}).get('options', [])
  options = next((e for e in options if e.name == msg.focused.name), {}).get('autocompleteOptions', [])

  if callable(options): options = options()
  if isinstance(options, dict): return [options[:25]]
  if isinstance(options, str): return [response(options)]
  return list(map(response, filter(
      lambda e: msg.focused.value.lower() in (e if hasattr(e, 'lower') else e.value).lower(), options[:25]
  )))
