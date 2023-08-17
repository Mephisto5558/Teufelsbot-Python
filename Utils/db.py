# https://github.com/Mephisto5558/Teufelsbot/blob/main/Utils/db.js

import json
from typing import overload
import oracledb

from config import logger, FlatDict

class DB:
  """
  Oracle Database, KEY-VALUE System\n
  In all methods that accept a `key` param, `key` is expected to be a string of keys separated with `key_separator`
  """

  # pylint: disable-next=too-many-arguments
  def __init__(self, db_connection_str: str, value_logging_max_json_length: int | None = 20, pool_min=1, pool_max=4, key_separator='.'):
    self.value_logging_max_json_length = value_logging_max_json_length or 0
    self._cache = {}
    self.__key_sep = key_separator

    self._pool = oracledb.create_pool(
        dsn=db_connection_str,
        min=pool_min,
        max=pool_max,
        encoding='utf-8'
    )

    self.fetch_all()

  def _execute_query(self, statement: str, params: list | tuple | dict = (), **keyword_params):
    connection = self._pool.acquire()
    cursor = connection.cursor()

    if keyword_params: cursor.execute(statement=statement, **keyword_params)
    else: cursor.execute(statement=statement, parameters=params)

    result = cursor.fetchall()
    cursor.close()

    connection.commit()
    self._pool.release(connection)

    return result

  def fetch_all(self):
    tables = self._execute_query('SELECT table_name FROM user_tables')
    for table, in tables:
      self._cache[table] = self.fetch(table)

    return self

  def fetch(self, table: str):
    """Note that there is NO VALIDATION of table names, so don't let the user put an SQL injection there"""

    result = self._execute_query(f'SELECT key, value FROM {table}')
    value = {row[0]: row[1] for row in result}
    self._cache[table] = value
    return value

  def create(self, table: str):
    """Note that there is NO VALIDATION of table names, so don't let the user put an SQL injection there"""

    self._execute_query(f'CREATE TABLE {table}(key VARCHAR2(200) NOT NULL, value VARCHAR2(2000))')
    self._cache[table] = {}
    return self

  @overload
  def get(self, table: str) -> FlatDict: ...
  @overload
  def get(self, table: str, key: None) -> FlatDict: ...  # type: ignore

  def get(self, table: str, key: str | None = None) -> str | int | bool | float | FlatDict | None:
    data = self._cache.get(table)
    if not key or not data: return data

    for obj_key in key.split(self.__key_sep):
      if not isinstance(data, dict): return data
      data = data.get(obj_key)
      if data is None: return None

    return data

  def set(self, table: str, key: str | None, value):
    """Note that there is NO VALIDATION of table names, so don't let the user put an SQL injection there"""

    self._save_log(f'Setting {table}{self.__key_sep}{key}' if key else f'Setting {table}', value)

    for attr, val in self._flatten_dict(value).items() if isinstance(value, dict) else ['', value]:
      if key and attr: key = f'{key}{self.__key_sep}{attr}'
      elif attr: key = attr

      self._execute_query(f"INSERT INTO {table}(key, value) VALUES (':key', :value)", key=key, value=val)
      self._cache[table][key] = val
    return value

  def delete(self, table: str, key: str | None = None):
    """
    Note that there is NO VALIDATION of table names, so don't let the user put an SQL injection there
    If no key has been provided, will drop the database
    returns: True if data has been found & deleted, otherwise False
    """

    if key:
      self._save_log(f'Deleting {table}{self.__key_sep}{key}'if key else f'Deleting {table}')

      data = self._cache.get(table)
      if data and key in data:
        del data[key]

        self._execute_query(f"DELETE FROM {table} WHERE entity = ':entity'", entity=key)
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
    return FlatDict(items)

  def _save_log(self, msg: str, value=None):
    json_value = json.dumps(value) if value else None
    logger.debug(msg + (f', value: {json_value}' if json_value and self.value_logging_max_json_length >= len(json_value) else ''))

    return self._save_log
