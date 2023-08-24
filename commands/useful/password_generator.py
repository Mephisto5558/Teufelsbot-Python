# https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Useful/passwordgenerator.js

from secrets import choice

default_charset = ['abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?§$%&/\\=*\'"#*(){}[]']

def password_generator():
  count = int(input('Enter the number of passwords to generate: '))
  length = int(input('Enter the length of each password: '))
  exclude = input('Enter characters to exclude (if any): ')
  include = input('Enter characters to include (if any): ')

  charset = default_charset + list(include)
  charset = ''.join([char for char in charset if char not in exclude])
  password_list = []

  if not charset: return 'charsetEmpty'

  for _ in range(count):
    last_random_char = ''
    if (len(password_list) + length) > 1743:
      break

    random_chars = []
    for _ in range(length):
      random_char = choice(charset.strip(last_random_char))
      # Todo: check if necessary to implement: https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Useful/passwordgenerator.js#L47-L50
      random_chars.append(random_char)
    password = ''.join(random_chars)
    password_list.append(password)

  if len(charset) > 100: charset = charset[:97] + '...'
  return password_list, charset


if __name__ == '__main__': print(password_generator())
