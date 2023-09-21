def filter_empty(obj: dict):
  """Filters empty values recursively from the provided dictionary"""

  new_obj = {}
  for k, v in obj.items():
    if v is not None and not (isinstance(v, (dict, list, tuple)) and len(v) == 0):
      new_obj[k] = filter_empty(v) if isinstance(v, dict) else v
  return new_obj
