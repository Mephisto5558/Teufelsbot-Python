from requests import get

from utils import Command

class Advice(Command):
  name = 'advice'
  slash_command = True
  prefix_command = True
  dm_permission = True

  def run(self, msg, _):
    data = get('https://api.adviceslip.com/advice', timeout=10).json()
    return msg.custom_reply(data['slip'].get('advice', None))
