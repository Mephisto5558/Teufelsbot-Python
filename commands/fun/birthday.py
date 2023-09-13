from utils import Command, Option, Cooldowns, get_age
from datetime import datetime

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

  def run(self, msg, lang):
    target = msg.options.get_member('target')
    do_not_hide = msg.options.getBoolean('do_not_hide')

    match(msg.options.get_subcommand()):
      case 'set':
        msg.client.db.set(
            'USERSETTINGS',
            f'{msg.user.id}.birthday',
            f"{msg.options.get_integer('year')}/{msg.options.get_integer('month'):02}/{msg.options.get_integer('day'):02}"
        )

        return msg.edit_eeply(lang('saved'))  # Todo: maybe add "your birthday is in <d> days"

      case 'remove':
        msg.client.db.delete('USERSETTINGS', f'{msg.user.id}.birthday')
        return msg.edit_reply(lang('removed'))

      case 'get':
        embed = EmbedBuilder(color=Colors.Burple, footer_text=msg.user.username, footer_icon_url=msg.member.display_avatar_url())

        if target:
          embed.data.title = lang('get_user.embed_title', msg.user.custom_tag)

          data = target.user.db['birthday'].split('/')
          if data:
            age = get_age(data) + 1
            embed.data.description = lang('get_user.date', user=target.custom_name, month=lang(f'months.{data[1]}'), day=data[2])
            if age < current_year: embed.data.description += lang('get_user.new_age', age)
          else: embed.data.description = lang('get_user.not_found', target.custom_name)
        else:
          embed.data.title = lang('get_all.embed._title')

          guild_members = [e.id for e in msg.guild.members.fetch()]
          current_time = datetime.now()
          data = sorted(
              [
                  (k, *v['birthday'].split('/'))
                  for k, v in msg.client.db.get('USERSETTINGSS')
                  if 'birthday' in v and k in guild_members
              ],
              key=lambda x:
              datetime(current_year, int(x[2]), int(x[3])) if datetime(current_year, int(x[2]), int(x[3])) >= current_time
              else datetime(current_year + 1, int(x[2]), int(x[3]))
          )[:10]

        embed.data.description = '' if data else lang('get_all.not_found')

        for id_, year, month, day in data:
          date = lang('get_all.date', month=lang(f'months.{month}'), day=day)
          age = get_age([year, month, day]) + 1
          msg = f"> <@{id_}>{' (' + str(age) + ')' if age < current_year else ''}\n"

          embed.data.description += msg if date in embed.data.description else f'\n{date}{msg}'

    if not do_not_hide: return msg.edit_reply(embeds=[embed])

    msg.channel.send(embed=[embed])
    return msg.edit_reply(lang('global.message_sent'))
