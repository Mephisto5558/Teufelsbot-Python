import json
from os import listdir
from os.path import isdir, isfile, join, splitext
from re import sub
from secrets import choice
from typing import Literal, overload

from .box import box
from .logger import log


class I18nProviderConfig(dict):  # pylint: disable-next=too-many-arguments
  def __init__(self, locales_path: str, default_locale: str, separator: str, not_found_message: str, error_not_found: bool, none_not_found: bool):
    self.locales_path = locales_path
    self.default_locale = default_locale
    self.separator = separator
    self.not_found_message = not_found_message
    self.error_not_found = error_not_found
    self.none_not_found = none_not_found


class I18nProvider:
  def __init__(  # pylint: disable=too-many-arguments
      self,
      locales_path='locales', default_locale='en', separator='.',
      not_found_message='', error_not_found=False, none_not_found=False
  ):
    self.config = I18nProviderConfig(
        locales_path=locales_path, default_locale=default_locale, separator=separator,
        not_found_message=not_found_message, error_not_found=error_not_found, none_not_found=none_not_found
    )

    self.locale_data = box()
    self.default_locale_data = box()
    self.available_locales: dict[str, str] = {}

    self.load_all_locales()

  def _load_files(self, path: str):
    data = {}

    for item in listdir(path):
      full_path = join(path, item)

      if isdir(full_path):
        data[item.lower()] = self._load_files(full_path)
      elif isfile(full_path):
        if not item.endswith('.json'):
          continue

        with open(full_path, encoding='utf-8') as file:
          # try:
          data[splitext(item)[0]] = json.load(file)
          # except json.JSONDecodeError:
          #   file.seek(0)
          #   data[splitext(item)[0]] = json.loads(file.read())

    return data

  def load_locale(self, locale: str):
    if not locale: return

    file_path = self.available_locales[locale]
    self.locale_data[locale] = self._load_files(file_path)

  def load_all_locales(self):
    for item in listdir(self.config.locales_path):
      full_path = join(self.config.locales_path, item)
      if '.ignore' not in listdir(full_path):
        self.available_locales[splitext(item)[0]] = full_path

    for locale in self.available_locales: self.load_locale(locale)

    data = self.locale_data[self.config.default_locale]
    if not data or isinstance(data, str):  # isinstance is a type guard
      raise FileNotFoundError(
          f'There are no valid language files for the default locale ({self.config.default_locale}) in the supplied locales path!')

    self.default_locale_data = box(data)

  @overload
  def __(self, key: str, locale: str | None = None, error_not_found: Literal[False] | None = None, none_not_found: Literal[True] = True,
         backup_path: str | None = None, replacement_all: str | None = None, **kw_replacements: str) -> str | None: ...

  @overload
  def __(self, key: str, locale: str | None = None, error_not_found: Literal[False] = False, none_not_found: Literal[False] = False,
         backup_path: str | None = None, replacement_all: str | None = None, **kw_replacements: str) -> str: ...

  @overload
  def __(self, key: str, locale: str | None = None, error_not_found: Literal[True] = True, none_not_found: bool | None = None,
         backup_path: str | None = None, replacement_all: str | None = None, **kw_replacements: str) -> str: ...

  def __(self, key: str, locale: str | None = None, error_not_found: bool | None = None, none_not_found: bool | None = None,
         backup_path: str | None = None, replacement_all: str | None = None, **kw_replacements: str):
    """
    Args:
        locale (str | None): the locale code to use. Defaults to `config.default_locale`.
        error_not_found (bool | None): if we should raise an `KeyError` if the key has not been found. Defaults to `config.error_not_found`.
        none_not_found (bool | None): if we should return `None` if the key has not been found. Gets ignored if `error_not_found` is True, ignoring of its default value. Defaults to `config.none_not_found`.
        backup_path (str | None): An alternative path that gets put in front of the `key` if the key has not been found.
        key (str): The key to look for.
        replacement_all (str | None): Replaces all {} what are not covered by `kw_replacements`

    Raises:
        KeyError: See doc on `error_not_found` and `none_not_found`
    """

    if not key: return ''

    original_error_not_found = error_not_found
    original_none_not_found = none_not_found
    if not locale: locale = self.config.default_locale
    if error_not_found is None: error_not_found = self.config.error_not_found
    if none_not_found is None: none_not_found = self.config.none_not_found

    message = self.locale_data.get(f'{locale}.{key}', self.locale_data[f'{locale}.{backup_path}.{key}'])
    if not message:
      if not none_not_found:
        log.warning('Missing "%s" localization for %s%s!', locale, key, (f' ({backup_path}.{key})' if backup_path else ''))
      if self.config.default_locale != locale:
        message = self.default_locale_data.get(key, self.default_locale_data[f'{backup_path}.{key}'])

    if isinstance(message, list): message = choice(message)

    if not message:
      if original_error_not_found or (error_not_found and original_none_not_found is False): raise KeyError(
          f'Key not found: "{key}"' + f'({backup_path}.{key})' if backup_path else '')
      if none_not_found: return None

      log.warning('Missing default ("%s") localization for %s%s!', locale, key, (f' ({backup_path}.{key})' if backup_path else ''))
      return self.config.not_found_message.format(key=key)

    return sub(r'{(\w+)}', lambda match: str(kw_replacements[match.group(1)] if match.group(1) in kw_replacements else replacement_all), message)

  def find_missing(self, check_equal: bool) -> dict[str, list[str]]:
    missing = {}

    for locale, in self.available_locales:
      missing[locale] = []
      for key in self.default_locale_data:
        if not self.locale_data[f'{locale}.{key}'] or (
            check_equal and self.config.default_locale != locale and
            self.locale_data[f'{locale}.{key}'] == self.default_locale_data[key]
        ): missing[locale].append(key)

    return {lang: entries for lang, entries in missing.items() if entries}

i18n_provider = I18nProvider(not_found_message='TEXT_NOT_FOUND: {key}', locales_path='locales')
