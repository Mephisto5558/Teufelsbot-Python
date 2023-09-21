from __future__ import annotations
from typing import TYPE_CHECKING
from asyncio import sleep
from time import time
from datetime import datetime

from discord import Message, AuditLogEntry, AuditLogAction, Embed, TextChannel

from utils import i18n_provider, better_partial
if TYPE_CHECKING:
  from main import MyClient

async def run(client: MyClient, messages: list[Message], channel: TextChannel):
  setting = client.db.get('GUILD_SETTINGS', f'{channel.guild.id}.config.logger.message_delete') or {} if channel.guild else None
  if client.bot_type == 'dev' or not channel.guild or not setting.get('enabled') or not setting.get('channel'):
    return None

  channel_to_send: TextChannel | None = channel.guild.channels[setting.channel]
  if (
      not channel_to_send or not channel_to_send.permissions_for(channel.guild.members.me).send_messages
      or not channel_to_send.permissions_for(channel.guild.members.me).embed_links
  ):
    return None

  await sleep(1)  # Making sure the audit log gets created before trying to fetching it

  lang = better_partial(
      i18n_provider.__,
      locale=client.db.get('GUILD_SETTINGS', f'{channel.guild.id}.config.lang')
      or channel.guild.local_code, backup_path='events.logger.message_delete_bulk'
  )
  audit_log: AuditLogEntry = next(
      [e async for e
       in channel.guild.audit_logs(limit=6, action=AuditLogAction.message_bulk_delete)
       if e.extra.channel.id == channel.id and e.extra.count == len(messages) and time() - e.created_at < 20000],
      default={}
  )

  embed = Embed(
      description=lang(
          'embed_description',
          executor=audit_log.user.mention if audit_log.user else lang('events.logger.someone'),
          channel=channel.name, count=str(len(messages))
      ),
      timestamp=datetime(),
      color=0xed498d
  ).add_field(name=lang('global.channel'), value=f'{channel.mention} (`{channel.id}`)', inline=False)

  if audit_log.user:
    embed.set_author(name=audit_log.user.name, icon_url=audit_log.user.name)
    embed.add_field(name=lang('events.logger.executor'), value=f'{audit_log.user.name} (`${audit_log.user.id}`)', inline=False)

  if audit_log.reason:
    embed.add_field(name=lang('events.logger.reason'), value=audit_log.reason, inline=False)

  return channel_to_send.send(embed=embed)
