# pylint: disable-next = no-name-in-module # false positive in git action
from typing import Any, Callable, NotRequired

from .i18n_provider import i18n_provider
from .logger import log

MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 32
MIN_DESC_LENGTH = 2
MAX_DESC_LENGTH = 100
MAX_CHOICE_NAME_LENGTH = 32

class Aliases(dict):
  """alias values must be between 2 and 32 chars"""

  def __init__(self, prefix: list[str] | None = None, slash: list[str] | None = None):
    self.prefix = prefix or []
    self.slash = slash or []

class Permissions(dict):
  client: NotRequired[list[str]] = []
  user: NotRequired[list[str]] = []

  def __init__(self, client: list[str] | None = None, user: list[str] | None = None):
    self.client = client or []
    self.user = user or []

class Cooldowns(dict):
  """Cooldowns in milliseconds"""

  def __init__(self, guild: int | float = 0, user: int | float = 0):
    self.guild = int(guild or 0)
    self.user = int(user or 0)

class Choice(dict):
  def __init__(self, key: str, value: str | int, name_localizations: dict[str, str] | None = None):
    self.key = key
    self.value = value
    self.name_localizations = name_localizations

class Option(dict):  # pylint: disable=too-many-instance-attributes
  @property
  def description_localizations(self):
    """Do not set manually."""
    return self._description_localizations
  _description_localizations: dict[str, str] | None
  "Do not set manually."

  def __init__(
      self, name: str, type: str, description: str | None = None, cooldowns: Cooldowns | None = None, required: bool = False,
      autocomplete_options: list[str | int | dict[str, str | int]] | Callable[[Any], list[str | int | dict[str, str | int]] | str | int] | None = None, strict_autocomplete: bool = False,
      channel_types: list[str] | None = None,
      min_value: int | None = None, max_value: int | None = None, min_length: int | None = None, max_length: int | None = None,
      options: list['Option'] | None = None, choices: list[Choice | dict[str, str | int] | str | int] | None = None
  ):
    self.name = name
    self.type = type
    self.description = description or None
    cooldowns = cooldowns or Cooldowns()
    self.required = required or False
    self.autocomplete_options = autocomplete_options or []
    self.strict_autocomplete = strict_autocomplete or False
    self.channel_types = channel_types if self.type == 'Channel' else None
    self.min_value = min_value if self.type == 'Integer' else None
    self.max_value = max_value if self.type == 'Integer' else None
    self.min_length = min_length if self.type == 'String' else None
    self.max_length = max_length if self.type == 'String' else None
    self.options = options or []
    self.choices = choices or []

class Command:
  name: str
  alias_of: NotRequired[str | None] = None
  type: str
  "The command name, must be between 2 and 32 chars"
  description: NotRequired[str] = ''

  @property
  def description_localizations(self):
    """Do not set manually."""
    return self._description_localizations
  _description_localizations: dict[str, str] = {}
  "Do not set manually."

  category: str
  aliases: NotRequired[Aliases] = Aliases()
  permissions: NotRequired[Permissions] = Permissions()
  cooldowns: NotRequired[Cooldowns] = Cooldowns()
  slash_command: bool = False
  prefix_command: bool = False
  dm_permission: NotRequired[bool] = False
  disabled: NotRequired[bool] = False
  no_defer: NotRequired[bool] = False
  ephemeral_defer: NotRequired[bool] = False
  beta: NotRequired[bool] = False
  options: NotRequired[list[Option]] = []

  # def __getitem__: # Todo

  @staticmethod
  def _name_formatter(name: str, path: str):
    if not name or not isinstance(name, str) or len(name) < MIN_NAME_LENGTH:
      raise TypeError(f'name ({path}.name) must be a string with at least {MIN_NAME_LENGTH} chars!')
    if len(name) > MAX_NAME_LENGTH:
      log.warning('name (%s.name) must not be longer then %i chars! Slicing', path, MAX_NAME_LENGTH)
      name = name[:MAX_NAME_LENGTH]
    if not name.islower():
      log.warning('name (%s.name) has uppercase letters! Fixing', path)
      name = name.lower()

    return name

  @staticmethod
  def _description_formatter(description: str | None, path: str):
    if not description:
      description = i18n_provider.__(f'{path}.description', error_not_found=True)
    if not description or not isinstance(description, str):
      raise TypeError(f'description ({path}.description) must be a string with at least {MIN_DESC_LENGTH} chars!')
    if len(description) > MAX_DESC_LENGTH:
      log.warning('description (%s.description) must not be longer then %i chars! Slicing', path, MAX_NAME_LENGTH)
      description = description[:MAX_DESC_LENGTH]

    return description

  @staticmethod
  def _description_localizer(path: str) -> dict[str, str]:
    locale_texts = {}
    for locale, in filter(lambda e, : e != i18n_provider.config['default_locale'], i18n_provider.available_locales):
      locale_text = i18n_provider.__(f'{path}.description', locale=locale, none_not_found=True)

      if not locale_text:
        log.warning('Missing "%s" description localization for option %s.description', locale, path)
        continue

      if len(locale_text) > MAX_DESC_LENGTH:
        log.warning('"%s" description localization of option %s.description is too long (max length is 100)! Slicing.', locale, path)
        locale_texts[locale] = locale_text[:MAX_DESC_LENGTH]

    return locale_texts

  @staticmethod
  def _choice_formatter(choices: list[Choice | dict[str, str | int] | str | int], path: str):
    for i, choice in enumerate(choices):
      locale_texts = {}

      for locale in filter(lambda e, : e != i18n_provider.config['default_locale'], i18n_provider.available_locales):
        locale_text = i18n_provider.__(f'{path}.{i}', locale=locale, none_not_found=True)
        if not locale_text:
          log.warning('Missing "%s" choice localization for option %s.%i', locale, path, i)
          continue

        if len(locale_text) > MAX_CHOICE_NAME_LENGTH: log.warning(
            '"%s" choice localization of option %s.%i is too long (max length is %i)! Slicing.',
            locale, path, i, MAX_CHOICE_NAME_LENGTH
        )

        locale_texts[locale] = locale_text[:MAX_CHOICE_NAME_LENGTH]

      if type(choice) is dict:  # pylint: disable=unidiomatic-typecheck
        name_localizations = choice.get('name_localizations', None)
        choice = Choice(
            key=str(choice.get('key', '')),
            value=choice.get('value', ''),
            name_localizations=name_localizations if isinstance(name_localizations, dict) else locale_texts
        )

      if isinstance(choice, Choice):
        if not choice.name_localizations: choice.name_localizations = locale_texts
        choices[i] = choice
      elif isinstance(choice, (int, str)): choices[i] = Choice(
          key=str(choice),
          value=i18n_provider.__(f'{path}.{i}', none_not_found=True) or choice,
          name_localizations=locale_texts
      )
      else: raise TypeError(choice)
    return choices

  @staticmethod
  def _options_formatter(option: Option, path: str):
    option.name = Command._name_formatter(option.name, path)
    # option.type =
    option.description = Command._description_formatter(option.description, path)
    option._description_localizations = Command._description_localizer(path)  # pylint: disable=protected-access

    if option.choices: option.choices = Command._choice_formatter(option.choices, f'{path}.choices')

  def __init__(self):
    path = f'commands.{self.category.lower()}.{self.name.lower()}'

    # TYPE
    # Todo: implement self.type

    if not self.category:
      raise TypeError(f'category ({path}.category) must be a non-empty string!')

    self.name = self._name_formatter(self.name, path)
    self.description = self._description_formatter(self.description, path)
    self._description_localizations = self._description_localizer(path)

    if not self.aliases.prefix: self.aliases.prefix = []
    if not self.aliases.slash: self.aliases.slash = []

    for i, alias in enumerate(self.aliases.slash):
      if not isinstance(alias, str) or len(alias) < MIN_NAME_LENGTH:
        log.warning('slash alias (%s[%i]) must be a string with at least %i chars! Ignoring', path, i, MIN_NAME_LENGTH)
        self.aliases.slash.remove(alias)
      elif len(alias) > MAX_NAME_LENGTH:
        log.warning('slash alias (%s[%i]) must not be longer then %i chars! Slicing', path, i, MAX_NAME_LENGTH)
        self.aliases.slash[i] = alias[:MAX_NAME_LENGTH]

    # PERMISSIONS
      # Todo: Implement permission conversion

    for option in self.options:
      option = self._options_formatter(option, f'{path}.options.{option.name}')

  def run(self, msg, lang):
    raise NotImplementedError('Subclasses must implement the run method')
