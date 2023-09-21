from __future__ import annotations
from typing import Any, TYPE_CHECKING
from asyncio import sleep
from time import time
from datetime import datetime

from discord import AllowedMentions, Message, AuditLogEntry, AuditLogAction, Embed, TextChannel

from utils import i18n_provider, better_partial
if TYPE_CHECKING:
  from main import MyClient

def check_if_int(maybe_int: Any):
  try:
    int(maybe_int)
    return True
  except ValueError:
    return False

async def counting_handler(client: MyClient, message: Message):
  counting_data = client.db.get('GUILD_SETTINGS', f'{message.channel.id}.counting_data') or {}
  if counting_data.get('last_number') and check_if_int(message.content): return message.channel.send(
      content=f"<t:{round(message.created_at / 1000)}>\n<@${message.user.id}>: *${counting_data['last_number']} -> {message.content}*",
      allowed_mentions=AllowedMentions.none()
  )

async def run(client: MyClient, message: Message):
  if client.bot_type == 'dev' or not message.guild: return None

  counting_handler(client, message)

  setting = client.db.get('GUILD_SETTINGS', f'{message.guild.id}.config.logger.message_delete') or {} if message.guild else None
  if client.bot_type == 'dev' or not message.guild or not setting['enabled'] or not setting['channel']:
    return None

  channel_to_send: TextChannel | None = message.guild.channels[setting.channel]
  if (
      not channel_to_send or not channel_to_send.permissions_for(client.user).send_messages
      or not channel_to_send.permissions_for(client.user).embed_links
  ):
    return None

  await sleep(1)  # Make sure the audit log gets created before trying to fetching it

  lang = better_partial(
      i18n_provider.__,
      locale=client.db.get('GUILD_SETTINGS', f'{message.guild.id}.config.lang')
      or message.guild.local_code, backup_path='events.logger.message_delete'
  )
  audit_log: AuditLogEntry = next(
      [e async for e
       in message.guild.audit_logs(limit=6, action=AuditLogAction.message_delete)
       if e.extra.channel.id == message.channel.id and (not e.user or not message.author or e.user.id == message.author.id) and time() - e.created_at < 20000],
      default={}
  )

  embed = Embed(
      description=lang(
          'embed_description',
          executor=audit_log.user.mention if audit_log.user else lang('events.logger.someone'),
          channel=message.channel.name
      ),
      timestamp=datetime(),
      color=0x822aed
  ) \
      .add_field(name=lang('global.channel'), value=f'{message.channel.mention} (`{message.channel.id}`)', inline=False) \
      .add_field(name=lang('content'), value='', inline=False)

  if message.content: embed.fields[1].value += f'{message.content}\n'
  if message.attachments: embed.fields[1].value += ', '.join(f'[{e.url}]({e.filename})' for e in message.attachments) + '\n'
  if message.embeds: embed.fields[1].value += lang('events.logger.embeds', len(message.embeds)) + '\n'
  if message.components: embed.fields[1].value += lang('components', len(message.components))

  # We don't get the user/member if the message is not cached (at least in d.js)
  if message.user: embed.add_field(name=lang('author'), value=f'{message.user.username} (`{message.user.id}`)', inline=False)
  if audit_log.user: embed.add_field(
      name=lang('events.logger.executor'),
      value=f'{audit_log.user.name} (`{audit_log.user.id}`)',
      inline=False
  )
  if audit_log.reason: embed.add_field(name=lang('events.logger.reason'), value=audit_log.reason, inline=False)

  return message.channel.send(embed=embed)
