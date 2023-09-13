from datetime import date


def get_age(date_param: tuple[int, int, int] | list[int]):
  """param date_param: A tuple representing the birth date in the format (year, month, day)."""

  today = date.today()
  birth_date = today.replace(year=date_param[0], month=date_param[1], day=date_param[2])
  age = today.year - birth_date.year

  if today < birth_date.replace(year=today.year): age -= 1

  return age


if __name__ == '__main__':
  try:
    year = int(input('Year:  '))
    month = int(input('Month: '))
    day = int(input('Day:   '))

    print(f'\nAge:   {get_age((year, month, day))}')
  except ValueError:
    print('Invalid Input')
