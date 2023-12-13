from datetime import datetime

from discord import Embed, Color, Interaction

from utils import Command, Option, Cooldowns, get_age

current_year = datetime.now().year

class CMD(Command):
  name = 'birthday'
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = False
  ephemeral_defer = True
  options = [
      Option(
          name='set',
          type='Subcommand',
          dm_permission=True,
          options=[
              Option(name='day', type='Integer', min_value=1, max_value=31, required=True),
              Option(name='month', type='Integer', min_value=1, max_value=12, required=True),
              Option(name='year', type='Integer', min_value=1900, max_value=current_year, required=True),
          ]
      ),
      Option(
          name='get',
          type='Subcommand',
          options=[
              Option(name='target', type='User'),
              Option(name='do_not_hide', type='Boolean')
          ]
      ),
      Option(name='remove', type='Subcommand', dm_permission=True)
  ]

  async def run(self, msg: Interaction, lang):
    target = msg.options.get_member('target')
    do_not_hide = msg.options.getBoolean('do_not_hide')

    match(msg.options.get_subcommand()):
      case 'set':
        msg.client.db.set(
            'USER_SETTINGS',
            f'{msg.user.id}.birthday',
            f"{msg.options.get_integer('year')}/{msg.options.get_integer('month'):02}/{msg.options.get_integer('day'):02}"
        )

        return msg.response.edit_message(content=lang('saved'))  # Todo: maybe add "your birthday is in <d> days"

      case 'remove':
        msg.client.db.delete('USER_SETTINGS', f'{msg.user.id}.birthday')
        return msg.response.edit_message(content=lang('removed'))

      case 'get':
        embed = Embed(color=Color.blurple()).set_footer(text=msg.user.name, icon_url=msg.member.display_avatar.url)

        if target:
          embed.title = lang('get_user.embed_title', msg.user.custom_tag)

          data = target.user.db['birthday'].split('/')
          if data:
            age = get_age(data) + 1
            embed.description = lang('get_user.date', user=target.custom_name, month=lang(f'months.{data[1]}'), day=data[2])
            if age < current_year: embed.description += lang('get_user.new_age', age)
          else: embed.description = lang('get_user.not_found', target.custom_name)
        else:
          embed.title = lang('get_all.embed_title')

          current_time = datetime.now()
          data = sorted(
              [
                  (k, *v['birthday'].split('/'))
                  for k, v in msg.client.db.get('USER_SETTINGS')
                  if 'birthday' in v and any(k == e.id for e in msg.guild.members)
              ],
              key=lambda x: (
                  datetime(current_year, int(x[2]), int(x[3])) if datetime(current_year, int(x[2]), int(x[3])) >= current_time
                  else datetime(current_year + 1, int(x[2]), int(x[3]))
              )
          )[:10]

        embed.description = '' if data else lang('get_all.not_found')

        for id_, year, month, day in data:
          date = lang('get_all.date', month=lang(f'months.{month}'), day=day)
          age = get_age([year, month, day]) + 1
          message = f"> <@{id_}>{' (' + str(age) + ')' if age < current_year else ''}\n"

          embed.description += message if date in embed.description else f'\n{date}{message}'

        if not do_not_hide: return msg.response.edit_message(embed=embed)

        msg.channel.send(embed=embed)
        return msg.response.edit_message(content=lang('global.message_sent'))
