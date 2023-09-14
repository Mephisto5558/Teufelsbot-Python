from utils import Aliases, Command, Option, Cooldowns

class CMD(Command):
  name = 'serverinfo'
  aliases = Aliases(prefix=['server-info', 'guildinfo', 'guild-info'])
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = True
  options = [Option(
      name='guild_id',
      type='String',
      autocomplete_options=lambda i: [g.id for g in i.client.guilds.cache if g.member.id in g.members.cache]
  )]

  def run(self, msg, lang):
    guild = msg.client.guild.cache.get(msg.options.get_string('guild_id') or msg.args[0]) or msg.guild
    channels = guild.channels.fetch().values()

    channels_count = {'text': 0, 'voice': 0, 'category': 0}
    for channel in guild.channels: channels_count[channel.type] += 1

    embed = EmbedBuilder(
        title=guild.name,
        description=guild.description,
        color=int(get_average_color(guild.icon_url()).hex[1:], 16),
        thumbnail={'url': guild.icon_url()},
        image={'url': guild.banner_url(size=1024)},
        fields=[
            {'name': lang('members'),
             'value': lang('memberStats', all=len(guild.members), humans=len([m for m in guild.members if not m.bot]), bots=len([m for m in guild.members if m.bot])),
             'inline': True},
            {'name': lang('verificationLevel.name'), 'value': lang(f'verificationLevel.{guild.verification_level}'), 'inline': True},
            {'name': lang('id'), 'value': f'`{guild.id}`', 'inline': True},
            {'name': lang('createdAt'), 'value': f'<t:{guild.created_timestamp}>', 'inline': True},
            {'name': lang('defaultNotifications.name'),
             'value': lang(f'defaultNotifications.{guild.default_notifications}'), 'inline': True},
            {'name': lang('owner'), 'value': f'<@{guild.owner_id}>', 'inline': True},
            {'name': lang('locale'), 'value': guild.preferred_locale, 'inline': True},
            {'name': lang('partnered'), 'value': lang(f'global.{guild.partnered}'), 'inline': True},
            {'name': lang('emojis'), 'value': f'`{len(guild.emojis)}`', 'inline': True},
            {'name': lang('roles'), 'value': f'`{len(guild.roles)}`', 'inline': True},
            {'name': lang('boosts.name'),
             'value': f"`{guild.premium_subscription_count}`{lang(f'boosts.{guild.premium_tier}') if guild.premium_tier else ''}", 'inline': True},
            {'name': lang('channels'),
             'value': ', '.join([f'{lang(f"others.ChannelTypes.plural.{k}")}: `{v}`' for k, v in channels_count.items()]), 'inline': False}
        ]
    )

    if guild.vanity_url_code:
      embed.data.fields.append({'name': lang('vanity_url'), 'value': guild.vanity_url_code, 'inline': True})
      embed.data.fields.append({'name': lang('vanity_url') + lang('uses'), 'value': guild.vanity_url_uses, 'inline': True})

    component = ActionRowBuilder(
        components=[ButtonBuilder(label=lang('download_icon'), style=ButtonStyle.Link, url=guild.icon_url(size=2048))]
    )

    if guild.banner: component.components.append(
        ButtonBuilder(label=lang('download_banner'), style=ButtonStyle.Link, url=guild.banner_url(size=2048))
    )

    return msg.custom_reply(embeds=[embed], components=[component])