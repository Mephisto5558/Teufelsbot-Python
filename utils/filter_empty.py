# https://github.com/Mephisto5558/Teufelsbot/blob/731991a54c3aceae1732ab739d44cd9d18f5cb29/Utils/prototypeRegisterer.js#L67-L70

def filter_empty(obj: dict):
  new_obj = {}
  for k, v in obj.items():
    if v is not None and not (isinstance(v, (dict, list, tuple)) and len(v) == 0):
      if isinstance(v, dict): new_obj[k] = filter_empty(v)
      else: new_obj[k] = v
  return new_obj
