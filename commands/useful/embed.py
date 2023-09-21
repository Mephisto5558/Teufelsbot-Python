from json import loads, dumps
from time import time

from discord import AllowedMentions, Interaction, Color, Embed, DiscordServerError

from utils import Command, Option, Cooldowns, Permissions, log_say_command_use

class CMD(Command):
  name = 'embed'
  permissions = Permissions(user=['Embed_links'])
  cooldowns = Cooldowns(user=200)
  slash_command = True
  prefix_command = False
  dm_permission = True
  ephemeral_defer = True
  options = [
      Option(
          name='custom',
          type='Subcommand',
          options=[
              Option(name='description', type='String', required=True),
              Option(name='content', type='String', max_length=2000),
              Option(name='title', type='String'),
              Option(
                  name='predefined_color',
                  type='String',
                  autocomplete_options=[k for k, v in Color.__dict__.items() if 'factory' in (v.__doc__ or '')],  # not very nice
                  strict_autocomplete=True
              ),
              Option(name='custom_color', type='String'),
              Option(name='footer_text', type='String'),
              Option(name='footer_icon', type='String'),
              Option(name='image', type='String'),
              Option(name='thumbnail', type='String'),
              Option(name='timestamp', type='Boolean'),
              Option(name='author_name', type='String'),
              Option(name='author_url', type='String'),
              Option(name='author_icon', type='String'),
              # Option(name='fields', type='String')
          ]
      ),
      Option(
          name='json',
          type='Subcommand',
          options=[Option(name='json', type='String', required=True)]
      )
  ]

  async def run(self, msg: Interaction, lang):
    def get_option(name: str) -> str:
      option = msg.options.get_string(name)
      return option.replace_all('/n', '\n') if option else ''

    custom = get_option('json')

    try:
      embed: Embed = Embed.from_dict(loads(custom) if custom else {
          'title': get_option('title'),
          'description': get_option('description'),
          'thumbnail': {'url': get_option('thumbnail')},
          'image': {'url': get_option('image')},
          'color': int(get_option('custom_color')[1:] or 0, 16) or get_option('predefined_color'),
          'footer': {'text': get_option('footer_text'), 'icon_url': get_option('footer_icon')},
          'timestamp': msg.options.get_boolean('timestamp') and round(time() / 1000),
          'author': {
              'name': get_option('author_name'),
              'url': get_option('author_url'),
              'iconURL': get_option('author_icon')
          }
          # fields: get_option('fields')
      })

      allowed_mentions = AllowedMentions(
          users=True, everyone=True, roles=True) if msg.user.resolved_permissions.mention_everyone else AllowedMentions(users=True)
      sent_message = await msg.channel.send(content=get_option('content') or None, embed=embed, allowed_mentions=allowed_mentions)
    except DiscordServerError as err:
      return msg.response.edit_message(lang('invalid_option', err.args[0]))

    await msg.edit_reply(lang('success_json') if custom else lang('success', dumps(embed.to_dict())))
    return log_say_command_use(sent_message, msg.user, lang)
