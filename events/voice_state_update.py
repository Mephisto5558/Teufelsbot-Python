from __future__ import annotations
from typing import TYPE_CHECKING
from time import time

from discord import Embed, VoiceState

from utils import i18n_provider, better_partial
if TYPE_CHECKING:
  from main import MyClient

async def run(client: MyClient, old_state: VoiceState, new_state: VoiceState):
  guild = old_state.channel.guild
  setting = (guild and client.db.get('GUILD_SETTINGS', f'{guild.id}.config.logger.voice_channel_activity')) or {}
  if client.bot_type == 'dev' or not guild or setting['enabled'] or not setting['channel'] or old_state.channel.id == new_state.channel.id:
    return None

  channel = guild.channels[setting.channel]
  if not channel or not channel.permissions_for(client.user).send_messages or not channel.permissions_for(client.user).embed_links:
    return None

  lang = better_partial(
      i18n_provider.__,
      locale=client.db.get('GUILD_SETTINGS', f'{guild.id}.config.lang')
      or guild.local_code, backup_path='events.logger.voice_state_update'
  )
  embed = Embed(timestamp=time(), color=0xe62aed).set_author(name=new_state.user.name, icon_url=new_state.user.display_avatar.url)

  if not old_state.channel:
    embed.description = lang('embed_description_join', executor=new_state.user.mention, new_channel=new_state.channel.name)
    embed.add_field(name=lang('new_channel'), value=f'{new_state.channel.mention} (`{new_state.channel.id}`)', inline=False)
  elif not new_state.channel:
    embed.description = lang(
        'embed_description_leave', executor=new_state.user.mention,
        old_channel=old_state.channel.name or lang('unknown')
    )
    if old_state.channel: embed.add_field(
        name=lang('old_channel'),
        value=f'{old_state.channel.mention} (`{old_state.channel.id}`)', inline=False
    )
  else:
    embed.description = lang(
        'embed_description_move', executor=new_state.user.mention,
        old_channel=old_state.channel.name or lang('unknown'), new_channel=new_state.channel.name
    )
    embed.add_field(name=lang('new_channel'), value=f'{new_state.channel.mention} (`{new_state.channel.id}`)', inline=False)
    if old_state.channel:
      embed.insert_field_at(0, name=lang('old_channel'), value=f'{old_state.channel.mention} (`{old_state.channel.id}`)', inline=False)

  return channel.send(embed=embed)
