# https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Fun/fact.js

from requests import get

def fact(lang: str = 'de'):
  data = get(f'https://uselessfacts.jsph.pl/api/v2/facts/random?language={lang}', timeout=10).json()
  if not data['text']: return None

  return f"{data['text']}\n\nSource: [{data['source']}]({data['source_url']})"


if __name__ == '__main__': print(fact())
