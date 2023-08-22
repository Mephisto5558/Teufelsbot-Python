class I18nProvider:
  def __init__(  # pylint: disable=too-many-arguments
      self,
      locales_path='locales', default_locale='en', separator='.',
      not_found_message='', error_not_found=False, none_not_found=False
  ):
    self.config = {
        'locales_path': locales_path, 'default_locale': default_locale, 'separator': separator,
        'not_found_message': not_found_message, 'error_not_found': error_not_found, 'none_not_found': none_not_found
    }

  def __(self, path: str, locale: str = '', error_not_found: bool = False, none_not_found: bool = True) -> str:
    if not locale: locale = self.config['default_locale']
    return ''

  available_locales: dict[str, str] = {}

i18n_provider = I18nProvider()
