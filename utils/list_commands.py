from discord import Interaction

from .command_class import Command
from .component_handler import filter_commands

def list_commands(i: Interaction) -> set[Command]:
  return {e for e in [*i.client.prefix_commands.values(), *i.client.slash_commands.values()] if filter_commands(i, e)}
