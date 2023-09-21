from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
  from main import MyClient
  from discord import Message, Interaction

def error_handler(client: MyClient, err: Exception, message: Message | Interaction, lang: Callable):
  pass
