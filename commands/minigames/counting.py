from utils import Command, Option, Cooldowns, Permissions, Colors

class CMD(Command):
  name = 'counting'
  permissions = Permissions(user=['ManageChannels'])
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = True
  options = [Option(name='channel', type='Channel', channel_types=Constants.TextBasedChannelTypes)]

  def run(self, msg, lang):
    channel = msg.options.get_channel('channel') or msg.mentions.channels.first() or msg.channel
    counting = msg.guild.db.counting or {}

    if counting[channel.id]:
      msg.client.db.delete('GUILDSETTINGS', f'{msg.guild.id}.counting.{channel.id}')

      embed = EmbedBuilder(
          description=lang('removed.embed_description'),
          footer={'text': lang('removed.by', msg.user.username)},
          color=Colors.Red
      )

      if msg.channel.id == channel.id: return msg.custom_reply(embeds=[embed])

      channel.send(embeds=[embed])
      return msg.custom_reply(lang('removed.success', channel.id))

    embed = EmbedBuilder(
        title=lang('added.embed_title'),
        description=lang('added.embed_description'),
        footer={'text': lang('added.by', msg.user.username)},
        colors=Colors.Green
    )

    msg.client.db.set('GUILDSETTINGS', f'{msg.guild.id}.counting.{channel.id}', {'lastNumber': 0})

    if msg.channel.id == channel.id: return msg.custom_reply(embeds=[embed])
    channel.send(embeds=[embed])

    return msg.custom_reply(lang('added.success', channel.id))
