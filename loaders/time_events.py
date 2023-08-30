from importlib import import_module
from os import listdir, path
from time import sleep
from threading import Thread

import schedule

from utils import log

def run_pending():
  while True:
    schedule.run_pending()
    sleep(10)
Thread(target=run_pending, name='time_events.run_pending')

def main(client):
  if client.bot_type == 'dev':
    log.info('Disabled timed events due to dev version.')
    return

  for file in listdir('time_events'):
    if not file.endswith('.py'): continue

    module = import_module(f'time_events.{path.splitext(file)[0]}')
    if hasattr(module, 'TIME') and hasattr(module, 'on_tick') and callable(module.on_tick):
      if hasattr(module, 'START_NOW'): module.on_tick(client)
      schedule.every().day.at(module.TIME).do(module.on_tick, client)

      log.info('Scheduled Time Event %s', file)
