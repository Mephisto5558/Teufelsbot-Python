from main import client

from .command_class import Command
from .component_handler import filter_commands

def list_commands(i=None) -> list[Command]:
  c = i if i else client
  return list(set(
      [e for e in c.prefix_commands.values() if filter_commands(e, i, client)]
      + [e for e in c.slash_commands.values() if filter_commands(e, i, client)]
  ))
