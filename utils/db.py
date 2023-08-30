# https://github.com/Mephisto5558/Teufelsbot/blob/main/Utils/db.js

import json

import oracledb
from box import Box

from .box import box
from .logger import log


class DB:
  """
  Oracle Database, KEY-VALUE System\n
  In all methods that accept a `key` param, `key` is expected to be a string of keys separated with `key_separator`
  """

  # pylint: disable-next=too-many-arguments
  def __init__(
      self, db_connection_str: str, value_logging_max_json_length: int | None = 20,
      pool_min=1, pool_max=4, key_separator='.', required_tables: list | None = None
  ):
    self.value_logging_max_json_length = value_logging_max_json_length or 0
    self._cache = box()
    self.__key_sep = key_separator

    self._pool = oracledb.create_pool(
        dsn=db_connection_str,
        min=pool_min,
        max=pool_max,
        encoding='utf-8'
    )

    self.fetch_all(required_tables)

  def _execute_query(self, statement: str, params: list | tuple | dict = (), **keyword_params):
    connection = self._pool.acquire()
    cursor = connection.cursor()

    if keyword_params: cursor.execute(statement=statement, **keyword_params)
    else: cursor.execute(statement=statement, parameters=params)

    try: result = cursor.fetchall()
    except oracledb.InterfaceError as err:
      if err.args[0].full_code == 'DPY-1003':  # "the executed statement does not return rows"
        return None
      raise

    cursor.close()

    connection.commit()
    self._pool.release(connection)

    return result

  def fetch_all(self, create_missing: list[str] | None):
    tables = [e[0] for e in self._execute_query('SELECT table_name FROM user_tables') or []]
    for table in tables:
      self._cache[table] = self.fetch(table)

    if isinstance(create_missing, list):
      for table in create_missing:
        if table.upper() not in tables: self.create(table)

    return self

  def fetch(self, table: str) -> Box:
    """Note that there is NO VALIDATION of table names, so don't let the user put an SQL injection there"""

    result = self._execute_query(f'SELECT key, value FROM {table}')

    self._cache[table] = {row[0]: row[1] for row in result} if result else {}
    return self._cache[table]

  def create(self, table: str):
    """Note that there is NO VALIDATION of table names, so don't let the user put an SQL injection there"""

    self._save_log(f'Creating table {table}')

    self._execute_query(f'CREATE TABLE {table}(key VARCHAR2(200) NOT NULL, value VARCHAR2(2000))')
    self._cache[table] = {}
    return self

  def get(self, table: str, key: str | None = None) -> str | int | bool | float | Box | None:
    data = self._cache.get(table)
    return data[key] if isinstance(data, Box) and key else data

  def set(self, table: str, key: str | None, value):
    """Note that there is NO VALIDATION of table names, so don't let the user put an SQL injection there"""

    self._save_log(f'Setting {table}{self.__key_sep}{key}' if key else f'Setting {table}', value)

    for attr, val in (self._flatten_dict(value).items() if isinstance(value, dict) else [['', value]]):
      if key and attr: key = f'{key}{self.__key_sep}{attr}'
      elif attr: key = attr

      self._execute_query(f"INSERT INTO {table}(key, value) VALUES (:key, :value)", key=key, value=val)
      self._cache[table][key] = val
    return value

  def delete(self, table: str, key: str | None = None):
    """
    Note that there is NO VALIDATION of table names, so don't let the user put an SQL injection there
    If no key has been provided, will drop the database
    returns: True if data has been found & deleted, otherwise False
    """

    if key:
      self._save_log(f'Deleting {table}{self.__key_sep}{key}')

      data = self._cache.get(table)
      if data and key in data:
        del data[key]

        self._execute_query(f"DELETE FROM {table} WHERE entity = :entity", entity=key)
        self._cache[table] = data
        return True
      return False

    self._save_log(f'Deleting {table}')

    self._execute_query(f'DROP TABLE {table}')
    return self._cache.pop(table, None) is not None

  def _flatten_dict(self, obj: dict, parent_key=''):
    items = []
    for k, v in obj.items():
      new_key = f'{parent_key}{self.__key_sep}{k}' if parent_key else k

      if isinstance(v, dict): items.extend(self._flatten_dict(v, new_key).items())
      else: items.append((new_key, v))
    return box(items)

  def _save_log(self, msg: str, value=None):
    json_value = json.dumps(value) if value else None
    log.debug(msg + (f', value: {json_value}' if json_value is not None and self.value_logging_max_json_length >= len(json_value) else ''))

    return self._save_log
