# https://github.com/Mephisto5558/Teufelsbot/blob/main/Utils/db.js

import oracledb
import logging
import json

class DB:
  def __init__(self, db_connection_str: str, value_logging_max_json_length: int|None=20, pool_min=1, pool_max=4):
    self._db_connection_string = db_connection_str
    self._cache = {}
    self.value_logging_max_json_length =  value_logging_max_json_length or 0

    self._pool = oracledb.create_pool(
      dsn=self._db_connection_string,
      min=pool_min,
      max=pool_max,
      encoding='UTF-8'
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
    result = self._execute_query('SELECT table_name FROM all_tables')
    for table, in result:
      self._cache[table] = self.fetch(table)
    
    return self

  def fetch(self, table: str):
    result = self._execute_query('SELECT attribute, value FROM :table', table=table)
    value = { row[0]: row[1] for row in result }
    self._cache[table] = value
    return value

  def create(self, table: str):
    self._execute_query(
      'CREATE TABLE :table(entity VARCHAR2(200) NOT NULL, attribute VARCHAR2(200) NOT NULL, value VARCHAR2(2000))',
      table=table
    )
    self._cache[table] = {}
    return self

  def get(self, table: str, key: str|None=None):
    data = self._cache.get(table)
    if key:
      for obj_key in key.split('.'):
        data = data.get(obj_key) if data else None
        if data is None: return None
    return data

  def set(self, table: str, key: str|None, value: dict|str):
    self._save_log(f'Setting {table}.{key}', value)
    
    for key, val in self._flatten_dict(value).items() if isinstance(value, dict) else value:
      self._execute_query(
        'INSERT INTO :table(entity, attribute, value) VALUES (:entity, :attribute, :value)',
        table=table, entity=table, attribute=key, value=val
      )
    
      self._cache[table][key] = val
    return value

  def delete(self, table: str, key: str|None=None):
    """returns: True if data has been found & deleted, otherwise False"""
    
    if key:
      self._save_log(f'Deleting {table}.{key}')
      
      data = self._cache.get(table)
      if data and key in data:
        del data[key]
        
        self._execute_query(
          'DELETE FROM :table WHERE entity = :entity AND attribute = :attribute',
          table=table, entity=table, attribute=key
        )
        self._cache[table] = data
        return True
      return False
      
    self._save_log(f'Deleting {table}')
      
    self._execute_query('DROP TABLE :table', table=table) 
    return self._cache.pop(table, None) is not None

  def _flatten_dict(self, obj: dict, parent_key='', sep='.'):
    items = []
    for k, v in obj.items():
      new_key = f'{parent_key}{sep}{k}' if parent_key else k
      
      if isinstance(v, dict): items.extend(self._flatten_dict(v, new_key, sep=sep).items())
      else: items.append((new_key, v))
    return dict(items)

  def _save_log(self, msg: str, value=None):
    json_value = json.dumps(value) if value else None
    logging.debug(msg + (f', value: {json_value}' if json_value and self.value_logging_max_json_length >= len(json_value) else ''))
    
    return self._save_log