from time import time, perf_counter
import asyncio
from utils import Command, Option, Cooldowns, Colors

class CMD(Command):
  name = 'ping'
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = True
  dm_permission = True
  beta = True
  options = [Option(name='average', type='Boolean')]

  async def run(self, msg, lang):
    average = msg.args[0] == 'average' or msg.options.get_boolean('average')
    embed = EmbedBuilder(
        title=lang('embed_title'),
        description=lang('average.loading' if average else 'global.loading', current=1, target=20),
        color=Colors.Green
    )

    start_message_ping = perf_counter()
    msg = await msg.custom_reply(embeds=[embed])
    end_message_ping = (perf_counter() - start_message_ping) * 1000

    if average:
      ws_pings = []
      msg_pings = [end_message_ping]

      for i in range(2, 21):
        ws_pings.append(msg.client.ws.ping)

        start_message_ping = perf_counter()
        await msg.edit(embeds=[embed.set_description(lang('average.loading', current=i, target=20))])
        msg_pings.append((perf_counter() - start_message_ping) * 1000)

        await asyncio.sleep(3)

      ws_pings.append(msg.client.latency * 1000)
      ws_pings.sort()
      msg_pings.sort()

      average_ws_ping = round(sum(ws_pings) / 20, 2)
      average_msg_ping = round(sum(msg_pings) / 20, 2)

      embed.description = lang(
          'average.embed_description',
          pings=len(ws_pings), ws_lowest=ws_pings[0], ws_highest=ws_pings[-1], ws_average=average_ws_ping,
          msg_lowest=round(msg_pings[0], 2), msg_highest=round(msg_pings[-1], 2), msg_average=average_msg_ping
      )
    else:
      embed.data.fields = [
          {'name': lang('api'), 'value': f'`{round(msg.client.ws.ping)}ms`', 'inline': True},
          {'name': lang('bot'), 'value': f'`{abs(time() * 1000 - msg.created_timestamp * 1000)}ms`', 'inline': True},
          {'name': lang('messageSend'), 'value': f'`{round(end_message_ping)}ms`', 'inline': True}
      ]

      del embed.data.description

    return msg.edit(embeds=[embed])
