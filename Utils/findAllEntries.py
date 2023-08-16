# https://github.com/Mephisto5558/Teufelsbot/blob/main/Utils/findAllEntries.js
# https://www.w3schools.com/python/ref_keyword_nonlocal.asp

def find_all_entries(obj, key):
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

if __name__ == '__main__':
  obj = {
    'a': 1,
    'b': {
      'a': 2,
      'b': { 'c': { 'a': 3 } }
    },
    'c': None
  }
  
  print(find_all_entries(obj, 'a'))