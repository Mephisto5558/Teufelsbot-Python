from .i18n_provider import i18n_provider


async def autocomplete_generator(msg, command, locale: str):
  def response(v):
    return {
        'name': i18n_provider.__(
            key=f"commands.{command.category.lower()}.{command.name}.options.{msg.options._group + '.' if msg.options._group else ''}{msg.options._subcommand + '.' if msg.options._subcommand else ''}{msg.focused.name}.choices.{v}",  # pylint: disable=protected-access
            locale=locale, none_not_found=True
        ) or v,
        'value': v
    }

  # pylint: disable=protected-access
  if msg.options._group:
    options = next((e for e in command.options if e.name == msg.options._group), None)
  if msg.options._subcommand:
    options = next(
        (e for e in command.options if e.name == msg.options._subcommand),
        {}).get('options', None)
  options = next((e for e in command.options if e.name == msg.focused.name), {}).get('autocompleteOptions', None)

  if callable(options): options = options()
  if isinstance(options, dict): return [options]
  if isinstance(options, str): return [response(options)]
  if isinstance(options, dict): return response(options[:25])
  return list(map(response, filter(
      lambda e: msg.focused.value.lower() in (e if hasattr(e, 'lower') else e.value).lower(), options[:25]
  )))
