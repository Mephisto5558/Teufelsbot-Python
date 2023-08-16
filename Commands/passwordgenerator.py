# https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Useful/passwordgenerator.js

from random import sample

defaultCharset = ['abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?§$%&/\\=*\'"#*(){}[]']

def passwordGenerator():
  count = int(input('Enter the number of passwords to generate: '))
  length = int(input('Enter the length of each password: '))
  exclude = input('Enter characters to exclude (if any): ')
  include = input('Enter characters to include (if any): ')

  charset = defaultCharset + list(include)
  charset = ''.join([char for char in charset if char not in exclude])
  passwordList = []

  if not charset: return 'charsetEmpty'

  for _ in range(count):
    oldRandomChar = ''
    if (len(passwordList) + length) > 1743: break

    randomChars = sample([char for char in charset if char != oldRandomChar], length)
    password = ''.join(randomChars)
    passwordList.append(password)

  if len(charset) > 100: charset = charset[:97] + '...'
  return passwordList, charset

if __name__ == '__main__': print(passwordGenerator())