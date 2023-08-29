from typing import TypeVar
from .i18n_provider import i18n_provider
_Perms = TypeVar('_Perms', str, list[str])

def permission_translator(perms: _Perms, locale: str) -> _Perms:
  if isinstance(perms, str): return i18n_provider.__(f'others.Perms.{perms}', locale) or perms
  return [i18n_provider.__(f'others.Perms.{perm}', locale) or perm for perm in perms]