from time import time


class application_command_option_type:
  subcommand = 0

def sub_command_cooldowns(msg, name: str) -> int:
  depth = len(name.split('.'))
  if depth >= 2:  # or not isinstance(msg, ChatInputCommandInteraction):
    return 0

  group_obj = None
  group = msg.options.get_subcommand_group(False)
  if group:
    cmd = msg.client.slash_commands.get(msg.command_name)
    if cmd and cmd.options and isinstance(cmd.options, list):
      group_obj = next(e.cooldowns for e in cmd.options if e.name == group and e.type == application_command_option_type.subcommand)
    if not depth and group_obj: return cooldowns(msg, f'{name}.{group}', group_obj)

  sub_cmd = msg.options.get_subcommand(False)
  if sub_cmd:
    cmd = group or msg
    if cmd and cmd.options and isinstance(cmd.options, list):
      sub_cmd_cooldowns = [
          e.cooldowns for e in cmd.options if e.name ==
          sub_cmd and e.type == application_command_option_type.subcommand
      ][0]
      if sub_cmd_cooldowns:
        return cooldowns(msg, f'{name}.{group}.{sub_cmd}' if group else f'{name}.{sub_cmd}', sub_cmd_cooldowns)

  return 0

def cooldowns(msg, name: str, cooldowns: dict[str, int|float]) -> int:
  guild = int(cooldowns.get('guild', 0))
  user = int(cooldowns.get('user', 0))

  if not guild and not user: return sub_command_cooldowns(msg, name)

  now = time() * 1000
  guild_timestamps, user_timestamps = msg.client.cooldowns.get(name) or msg.client.cooldowns.set(name, {'guild': {}, 'user': {}}).get(name)

  cooldown = 0
  if guild and msg.guild:
    guild_cooldown = guild_timestamps.get(msg.guild.id, None)
    if guild_cooldown and guild_cooldown > now:
      cooldown = max(cooldown, round(guild_cooldown - now) / 1000)
    else: guild_timestamps[msg.guild.id] = now + guild

    if user:
      user_cooldown = user_timestamps.get(msg.user.id, None)
      if user_cooldown and user_cooldown > now:
        cooldown = max(cooldown, round(user_cooldown - now) / 1000)
      else: user_timestamps[msg.user.id] = now + user

  return cooldown or sub_command_cooldowns(msg, name)
