from __future__ import annotations
from sys import exit  # pylint:disable=redefined-builtin
from typing import TYPE_CHECKING

from utils import log
if TYPE_CHECKING:
  from main import MyClient

def run(client: MyClient, debug: str):
  if 'Sending a heartbeat.' in debug or 'Heartbeat acknowledged' in debug: return None

  log.debug(debug)
  if 'Hit a 429' not in debug: return None

  if client.is_ready():
    return log.error('Hit a 429 while trying to execute a request')

  log.error('hit a 429 while trying to login. Killing bot.')
  exit(1)
