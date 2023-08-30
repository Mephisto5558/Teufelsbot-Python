from subprocess import CalledProcessError, run
from .logger import log


def git_pull():
  try:
    data = run('git pull', capture_output=True, text=True, check=True, shell=True)
  except CalledProcessError as err:
    log.error('Exec error: %s', err.stderr)
    return err

  if data.stdout: log.info('OUT: %s', data.stdout.strip())
  if data.stderr: log.info('ERR: %s', data.stderr.strip())

  return 'OK'
