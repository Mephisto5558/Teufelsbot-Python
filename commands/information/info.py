from json import load
from time import process_time, time

from utils import Command, Colors

with open('config.json', 'r', encoding='utf8') as file:
  config = load(file)

USERS_URL = 'https://discord.com/users'

class CMD(Command):
  name = 'info'
  slash_command = True
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    start_time = round(time() - process_time())
    description = (
        f"{lang('dev')}: [Mephisto5558]({USERS_URL}/691550551825055775)\n"
        + f"{lang('shard')}: `{msg.guild.shard_id}\n"
        + f"{lang('guild')}: `{msg.guild.db.postion or 0}`\n"
        + f"{lang('guilds')}: `{len(msg.client.guilds.cache)}`\n"
        + f"{lang('commands')}: `{len(set(e for e in msg.client.prefix_commands + msg.client.slash_commands if not e.alias_of))}`\n"
        + f"{lang('starts')}: `{msg.client.settings['start_count.'+ msg.client.bot_type] or 0}\n"
        + f"{lang('last_start')}: <t:{start_time}> (<t:{start_time}:R>)\n"
        + lang(
            'translation',
            de=f'[Mephisto5558]({USERS_URL}/691550551825055775) & [Koikarpfen1907]({USERS_URL}/636196723852705822)',
            en=f'[Mephisto5558]({USERS_URL}/691550551825055775) & [PenguinLeo]({USERS_URL}/740930989798195253)'
        )
        + lang('links', Invite=config.get('Invite'), Dashboard=config.get('Dashboard'), PrivacyPolicy=config.get('PrivacyPolicy'))
    )

    embed = EmbedBuilder(
        title=lang('embed_title'),
        description=description,
        color=Colors.DarkGold,
        footer={'text': lang('embed_footer_text')}
    )

    return msg.custom_reply(embeds=[embed])
