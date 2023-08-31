def check_target(msg, member):
  if member.id == msg.member.id: return 'cant_punish_self'
  if not member.bannable: return 'global.no_perm_bot'
  if msg.guild.owner_id != msg.user.id and member.roles.hightest.compare_position_to(msg.member.roles.hightest) > -1:
    return 'global.no_perm_user'
  return None
