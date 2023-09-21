def find_all_entries(obj: dict, key: str):
  if not obj or not key: return {}

  counter = 0
  entry_list = {}

  def find_entries(obj):
    nonlocal counter, entry_list

    if counter > 1000: return
    counter += 1

    for o_key, o_val in obj.items():
      if o_key == key:
        entry_list[key] = o_val
      elif isinstance(o_val, dict):
        data = find_all_entries(o_val, key)
        if data: entry_list[o_key] = data

  find_entries(obj)
  return entry_list
