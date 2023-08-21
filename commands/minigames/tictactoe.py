# https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Minigames/tictactoe.js

from random import choice

def print_board(board: list[list[str]]):
  print("\033[1m")
  for row in board:
    print(" | ".join(row))
    print("-" * 9)
  print("\033[0m")

def check_winner(board: list[list[str]]):
  for row in board:
    if row[0] == row[1] == row[2] != ' ':
      return row[0]

  for col in range(3):
    if board[0][col] == board[1][col] == board[2][col] != ' ':
      return board[0][col]

  if board[0][0] == board[1][1] == board[2][2] != ' ':
    return board[0][0]

  if board[0][2] == board[1][1] == board[2][0] != ' ':
    return board[0][2]

  return None

def play():
  board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
  current_player = choice(['X', 'O'])
  winner = None
  moves = 0

  while True:
    print_board(board)
    print(f'Currently playing: \033[1m\033[94m{current_player}\033[0m')

    try:
      row = int(input('Input row number (1-3):    ')) - 1
      col = int(input('Input column number (1-3): ')) - 1
    except ValueError:
      print('\033[91mInvalid move! Please enter a valid row and column number.\033[0m')
      continue

    if 0 <= row <= 2 and 0 <= col <= 2:
      if board[row][col] == ' ':
        board[row][col] = current_player
        current_player = 'O' if current_player == 'X' else 'X'
        moves += 1
      else:
        print('\033[91mInvalid move! The cell is already occupied.\033[0m')
    else:
      print('\033[91mInvalid move! Please enter a valid row and column number.\033[0m')

    winner = check_winner(board)
    if winner:
      print_board(board)
      print(f'The winner is: \033[92m{winner}\033[0m')
      break
    if moves == 9:
      print_board(board)
      print('\033[93mIt\'s a tie!\033[0m')
      break


if __name__ == '__main__': play()