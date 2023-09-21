from discord import Message, ActivityType

from utils import Command

class CMD(Command):
  name = 'setactivity'
  slash_command = False
  prefix_command = True
  dm_permission = True

  async def run(self, msg: Message, lang):
    args = msg.content.split(';')
    activity = args[0]
    activity_type = ActivityType.playing if not args[1] else next(e for e in ActivityType if e.name.lower() == args[1].lower())

    if not isinstance(activity_type, ActivityType): activity_type = ActivityType[activity_type]

    if not isinstance(activity_type, ActivityType):
      return msg.reply(lang('invalid_type', '`, `'.join(e.name for e in ActivityType)))

    msg.client.user.set_activity(activity, type=activity_type)
    msg.client.db.set('BOT_SETTINGS', 'activity', name=activity, type=activity_type)

    return msg.reply(lang('set', name=activity, type=activity_type) if activity else lang('reset'))
