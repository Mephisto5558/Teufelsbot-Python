from typing import DefaultDict, NotRequired, TypedDict, Callable
from utils import log, i18n_provider

MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 32
MIN_DESC_LENGTH = 2
MAX_DESC_LENGTH = 100
MAX_CHOICE_NAME_LENGTH = 32

class Aliases(DefaultDict):
  """alias values must be between 2 and 32 chars"""
  prefix: NotRequired[list[str]] = []
  slash: NotRequired[list[str]] = []

class Permissions(DefaultDict):
  client: NotRequired[list[str]] = []
  user: NotRequired[list[str]] = []

class Cooldowns(DefaultDict):
  """Cooldowns in milliseconds"""
  guild: NotRequired[tuple[()] | tuple[int, ...]] = ()
  user: NotRequired[tuple[()] | tuple[int, ...]] = ()

class Choice(TypedDict):
  key: str
  value: str | int
  name_localizations: dict[str, str]

class Option(DefaultDict):
  name: str
  type: str
  description: str

  @property
  def description_localizations(self):
    """Do not set manually."""
    return self._description_localizations
  _description_localizations: dict[str, str] = {}
  "Do not set manually."

  required: NotRequired[bool] = False
  autocomplete_options: NotRequired[tuple | Callable] = ()
  strict_autocomplete: NotRequired[bool] = False
  choices: NotRequired[list[str | int | Choice]] = []

class Command:
  name: str
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
  def _description_formatter(description: str, path: str):
    if not description:
      description = i18nProvider.__(f'{path}.description', error_not_found=True)
    if not description or not isinstance(description, str):
      raise TypeError(f'description ({path}.description) must be a string with at least {MIN_DESC_LENGTH} chars!')
    if len(description) > MAX_DESC_LENGTH:
      log.warning('description (%s.description) must not be longer then %i chars! Slicing', path, MAX_NAME_LENGTH)
      description = description[:MAX_DESC_LENGTH]

    return description

  @staticmethod
  def _description_localizer(path: str):
    locale_texts = {}
    for locale, in filter(lambda e, : e != i18nProvider.config.default_locale, i18nProvider.available_locales):
      locale_text = i18nProvider.__(f'{path}.description', locale=locale, none_not_found=True)

      if not locale_text:
        log.warning('Missing "%s" description localization for option %s.description', locale, path)
      elif len(locale_text) > MAX_DESC_LENGTH:
        log.warning('"%s" description localization of option %s.description is too long (max length is 100)! Slicing.', locale, path)

      locale_texts[locale] = locale_text[:MAX_DESC_LENGTH]
    return locale_texts

  @staticmethod
  def _choice_formatter(choices, path):
    for i, choice in enumerate(choices):
      locale_texts = {}
      for locale in filter(lambda e, : e != i18nProvider.config.default_locale, i18nProvider.available_locales):
        locale_text = i18nProvider.__(f'{path}.{i}', locale=locale, none_not_found=True)
        if not locale_text:
          log.warning('Missing "%s" choice localization for option %s.%i', locale, path, i)
        else:
          if len(locale_text) > MAX_CHOICE_NAME_LENGTH: log.warning(
              '"%s" choice localization of option %s.%i is too long (max length is %i)! Slicing.',
              locale, path, i, MAX_CHOICE_NAME_LENGTH
          )

          locale_texts[locale] = locale_text[:MAX_CHOICE_NAME_LENGTH]

      if isinstance(choice, dict): choices[i] = Choice(*choice, name_localizations=locale_texts)
      else: choices[i] = Choice(key=choice, value=i18nProvider.__(f'{path}.{i}', none_not_found=True) or choice, name_localizations=locale_texts)
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

    for i, option in enumerate(self.options):
      option = self._options_formatter(option, f'{path}.options[{i}]')

  def run(self, msg, lang: Callable):
    raise NotImplementedError('Subclasses must implement the run method')
