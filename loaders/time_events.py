from importlib import import_module
from os import listdir, path
from time import sleep

import schedule


def main(client):
  if client.botType == 'dev':
    print('Disabled timed events due to dev version.')
    return

  for file in listdir('TimeEvents'):
    if not file.endswith('.py'):
      continue

    module = import_module(f'TimeEvents.{path.splitext(file)[0]}')

    if hasattr(module, 'TIME') and hasattr(module, 'on_tick') and callable(module.on_tick):
      if hasattr(module, 'START_NOW'): module.on_tick(client)
      schedule.every().day.at(module.TIME).do(module.on_tick, client)

      print(f'Scheduled Time Event {file}')

while True:
  schedule.run_pending()
  sleep(10)
