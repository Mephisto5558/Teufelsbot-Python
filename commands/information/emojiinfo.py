from discord import Embed, ActionRow, Button, ButtonStyle

from utils import Aliases, Command, Option

class CMD(Command):
  name = 'emojiinfo'
  aliases = Aliases(prefix=['emoji-info'])
  slash_command = True
  prefix_command = True
  options = [Option(name='emoji', type='String', required=True)]

  def run(self, msg, lang):
    parsed_emoji = parse_emoji(msg.options.get_string('emoji') or msg.args[0] or '')
    emoji = msg.client.emojis.cache.get(parsed_emoji.id) or parsed_emoji

    if not emoji.id: return msg.custom_reply(content=lang('not_found'))
    if not emoji.url: emoji.url = f'https://cdn.discordapp.com/emojis/{emoji.id}.webp?size=2048'

    embed = Embed(
        title=lang('embed_title', f'<:{emoji.name}:{emoji.id}>'),
        color=int(get_average_color(emoji.url).hex[1:], 16)
    ) \
        .set_thumbnail(url=emoji.url) \
        .add_field([
            {'name': lang('name'), 'value': emoji.name, 'inline': True},
            {'name': lang('id'), 'value': emoji.id, 'inline': True},
            {'name': lang('guild'),
             'value': f'{emoji.guild.name} ({emoji.guild.id})' if emoji.guild and emoji.guild.name else lang('unknown'), 'inline': True},
            {'name': lang('animated'), 'value': lang(f'global.{emoji.animated}'), 'inline': True},
            {'name': lang('creator'), 'value': emoji.author.tag or lang('unknown'), 'inline': True},
            {'name': lang('available'), 'value': lang(f'global.{emoji.available}') if emoji.available else lang('unknown'), 'inline': True},
            {'name': lang('created_at'), 'value': f'<t:{round(emoji.created_timestamp / 1000)}>' if emoji.created_timestamp else lang('unknown'), 'inline': True},
            {'name': lang('requires_colons'),
             'value': lang(f'global.{emoji.requires_colons}') if emoji.requires_colons else lang('unknown'), 'inline': True},
        ])

    component = ActionRow(components=[Button(label=lang('download'), style=ButtonStyle.link, url=emoji.url)])

    if emoji.guild.id == msg.guild.id and msg.user.guild_permissions.manage_expressions:
      component.children.append(Button(
          label=lang('delete'), custom_id=f'info_cmds.{emoji.id}.delete.emojis', style=ButtonStyle.danger
      ))

    if emoji.roles.cache: embed.add_field(
        name=lang('allowed_roles'),
        value='<@&' + '> <@&'.join(e.id for e in emoji.roles.cache), inline=False
    )

    return msg.custom_reply(embed=embed, components=[component])
