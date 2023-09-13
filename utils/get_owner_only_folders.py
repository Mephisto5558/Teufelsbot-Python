from json import load, JSONDecodeError

def get_owner_only_folders() -> set[str]:
  """Reads from config.json and defaults to `['owner-only']`."""
  try:
    with open('config.json', 'r', encoding='utf8') as file:
      folders = load(file).get('owner_only_folders', None)
      return {str(folder).lower() for folder in folders} if folders else {'owner-only'}
  except (FileNotFoundError, JSONDecodeError):
    return {'owner-only'}
