def check_target(msg, member):
  if member.id == msg.member.id: return 'cantPunishSelf'
  if not member.bannable: return 'global.noPermBot'
  if msg.guild.owner_id != msg.user.id and member.roles.hightest.comparePositionTo(msg.member.roles.hightest) > -1:
    return 'global.noPermUser'
  return None
