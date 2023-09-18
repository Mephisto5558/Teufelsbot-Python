from utils import Command

class CMD(Command):
  name = 'setactivity'
  slash_command = False
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    args = msg.content.split(';')
    actitvity = args[0]
    activity_type = ActivityType.Playing if not args[1] else ActivityType[next(e for e in ActivityType if e.lower() == args[1].lower())]

    if not isinstance(activity_type, int): activity_type = ActivityType[activity_type]

    if not activity_type and activity_type != 0:
      return msg.reply(lang('invalid_type', '`, `'.join(e for e in ActivityType if isinstance(e, str))))

    msg.client.user.set_activity(actitvity, type=activity_type)
    msg.client.db.set('BOTSETTINGS', 'activity', name=actitvity, type=activity_type)

    return msg.reply(lang('set', name=actitvity, type=ActitvityType[actitvity]) if actitvity else lang('reset'))
