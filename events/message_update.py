from __future__ import annotations
from typing import TYPE_CHECKING
from time import time

from discord import Embed, ActionRow, Button, ButtonStyle, Message

from utils import i18n_provider, better_partial
if TYPE_CHECKING:
  from main import MyClient

def run(client: MyClient, old_msg: Message, new_msg: Message):
  setting = client.db.get('GUILD_SETTINGS', f'{old_msg.guild.id}.config.logger.message_update') or {}

  if (client.bot_type == 'dev' or not old_msg.guild or not setting['enabled'] or not setting['channel'] or all(
      [old_msg.content == new_msg.content, len(old_msg.attachments) == len(new_msg.attachments), len(old_msg.embeds), len(new_msg.embeds)]
  )):
    return None

  channel = old_msg.guild.channels[setting.channel]
  if not channel or channel.permissions_for(client.user).send_messages or channel.permissions_for(client.user).embed_links:
    return None

  lang = better_partial(
      i18n_provider.__,
      locale=client.db.get('GUILD_SETTINGS', f'{old_msg.guild.id}.config.lang')
      or old_msg.guild.local_code, backup_path='events.logger.message_update'
  )
  embed = Embed(
      description=lang('embed_description', executor=new_msg.user.mention, channel=new_msg.channel.name),
      timestamp=time(),
      color=0xe62aed
  ) \
      .set_author(name=new_msg.author.name, icon_url=new_msg.author.avatar.url) \
      .add_field(name=lang('global.channel'), value=f'{new_msg.channel.mention} ({new_msg.channel.id})', inline=False) \
      .add_field(name=lang('old_content'), value='', inline=False) \
      .add_field(name=lang('new_content'), value='', inline=False) \
      .add_field(name=lang('author'), value=f'{new_msg.user.name} ({new_msg.user.id})', inline=False)

  component = ActionRow(Button(label=lang('message_link'), url=new_msg.jump_url, style=ButtonStyle.link))

  if old_msg.content: embed.fields[1].value += f'{old_msg.originalContent}\n'
  if new_msg.originalContent: embed.fields[2].value += f'{new_msg.originalContent}\n'

  if old_msg.attachments: embed.fields[1].value += ', '.join([f'[{e.url}]({e.name})' for e in old_msg.attachments]) + '\n'
  if new_msg.attachments: embed.fields[2].value += ', '.join([f'[{e.url}]({e.name})' for e in new_msg.attachments]) + '\n'

  if old_msg.embeds: embed.fields[1].value += lang('events.logger.embeds', len(old_msg.embeds))
  if new_msg.embeds: embed.fields[2].value += lang('events.logger.embeds', len(new_msg.embeds))

  if embed.fields[1].value == '': embed.fields[1].value = lang('unknown')
  if embed.fields[2].value == '': embed.fields[2].value = lang('unknown')

  return channel.send(embed=embed, components=[component])
