from os import makedirs, scandir, unlink
from os.path import join, getmtime
from datetime import date, timedelta

from utils import log


def delete_old(path: str):
  makedirs(path, exist_ok=True)

  time = date.today() - timedelta(weeks=2)
  for file in scandir(path):
    file_path = join(path, file.name)

    if file.is_dir(): delete_old(file_path)
    elif date.fromtimestamp(getmtime(file_path)) < time:
      log.debug('deleting %s', file_path)
      unlink(file_path)


TIME = '00:00:00'
START_NOW = True

def on_tick(client):
  now = date.today().strftime('%m-%d')

  if client.settings.lastFileClear == now:
    log.info('Already ran file deletion today')
    return

  log.info('started file deletion')

  delete_old('./logs')

  client.db.set('BOT_SETTINGS', 'last_file_clear', now)
  log.info('Finished file deletion')
