from utils import Command, Option, Cooldowns

class CMD(Command):
  name = 'prefix'
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = True
  options = [
      Option(name='new_prefix', type='String'),
      Option(name='case_insensitive', type='String')
  ]

  def run(self, msg, lang):
    new_prefix = msg.content or msg.options.get_string('new_prefix')
    prefix_case_insensitive = msg.options.get_boolean('case_insensitive') or False

    if new_prefix and PermissionFlagsBits.ManageGuild in msg.member.permissions:
      msg.client.db.set(
          'GUILDSETTINGS',
          f"{msg.guild.id}.config.{'beta_bot_' if msg.client.bot_type == 'dev' else ''}prefix",
          {'prefix': new_prefix, 'caseinsensitive': prefix_case_insensitive}
      )

      return msg.custom_reply(lang('saved', new_prefix))

    current_prefix = msg.guild.db['config.prefix.prefix'] or msg.client.default_settings['config.prefix']
    if not current_prefix: raise KeyError('No default prefix found in DB')

    return msg.custom_reply(lang('current_prefix', current_prefix) + (lang('case_insensitive') if msg.guild.db.config['prefix.caseinsensitive'] else ''))
