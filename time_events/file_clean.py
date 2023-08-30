import os
from datetime import date, timedelta

from utils import log


def delete_old(path: str):
  os.makedirs(path, exist_ok=True)

  time = date.today() - timedelta(weeks=2)
  for file in os.scandir(path):
    file_path = os.path.join(path, file.name)

    if file.is_dir(): delete_old(file_path)
    elif date.fromtimestamp(os.path.getmtime(file_path)) < time:
      log.debug('deleting %s', file_path)
      os.unlink(file_path)


TIME = '00:00:00'
START_NOW = True

def on_tick(self):
  now = date.today().strftime('%m-%d')

  if self.settings.lastFileClear == now:
    log.info('Already ran file deletion today')
    return

  log.info('started file deletion')

  delete_old('./Logs')

  self.db.set('BOT_SETTINGS', 'lastFileClear', now)
  log.info('Finished file deletion')