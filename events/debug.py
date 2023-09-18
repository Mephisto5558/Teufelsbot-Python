from sys import exit  # pylint:disable=redefined-builtin
from utils import log

def run(client, debug: str):
  if 'Sending a heartbeat.' in debug or 'Heartbeat acknowledged' in debug: return None

  log.debug(debug)
  if 'Hit a 429' not in debug: return None

  if client.is_ready():
    return log.error('Hit a 429 while trying to execute a request')

  log.error('hit a 429 while trying to login. Killing bot.')
  exit(1)
