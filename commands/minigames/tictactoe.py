from discord import Interaction, Member

from utils import Command, Aliases, Permissions, Cooldowns, Option, DB

def event_callback(msg: Interaction, players: list[Member], types: list[str], lang, game):
  if msg.client.user.id in (players[0]['id'], players[1]['id']):
    return None

  update_stats(players[0].id, players[1].id, types[0], msg.client.db)
  update_stats(players[1].id, players[0].id, types[1], msg.client.db)
  return game.play_again(msg, lang)

def update_stats(first_id: str, second_id: str, type_: str, db: DB):
  stats = db.get('LEADERBOARDS', f'tic_tac_toe.{first_id}') or {}
  against = None

  if type_ == 'win': against = 'won_against'
  elif type_ == 'lose': against = 'lost_against'
  elif type_ == 'draw': against = 'drew_against'

  db.set('LEADERBOARDS', f'tic_tac_toe.{first_id}.games', stats.get('games', 0) + 1)
  db.set('LEADERBOARDS', f'tic_tac_toe.{first_id}.{type_}s', stats.get(f'{type_}s', 0) + 1)
  return db.set('LEADERBOARDS', f'Tic_tac_toe.{first_id}.against.{second_id}', stats.get(against, {}).get(second_id, 0) + 1)


class CMD(Command):
  name = 'tictactoe'
  aliases = Aliases(slash=['ttt'])
  permissions = Permissions(client=['manage_messages'])
  cooldowns = Cooldowns(user=5000)
  slash_command = True
  prefix_command = False
  options = [Option(name='opponent', type='user')]
  disabled = True  # game not implemented yet

  def run(self, msg: Interaction, lang):
    target = msg.options.get_user('opponent').id
    game = sth  # code for game lib

    if target: msg.channel.send(lang('new_challenge'), delete_after=5000)

    game.on('win', lambda data: event_callback(msg, [data.winner, data.loser], ['win', 'lose'], lang, game))
    game.on('tie', lambda data: event_callback(msg, data.players, ['draw'], lang, game))

    return game.handle_interaction(msg)
