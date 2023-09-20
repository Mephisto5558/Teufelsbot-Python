from __future__ import annotations
from typing import TYPE_CHECKING

from discord import ChannelType, Thread

if TYPE_CHECKING:
  from main import MyClient

def main(client: MyClient, thread: Thread):
  if (not thread.archived and not thread.joined and (
      thread.permissions_for(client.user).manage_threads
      if thread.type == ChannelType.private_thread
      else thread.permissions_for(client.user).read_messages
  )): thread.join()
