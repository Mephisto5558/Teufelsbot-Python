import logging
from datetime import date

class CustomFormatter(logging.Formatter):
  format_ = '%(asctime)s [%(levelname)s] %(module)s#%(lineno)d: %(message)s'

  FORMATS = {
      logging.DEBUG: '\033[38;5;33m' + format_ + '\033[0m',
      logging.INFO: '\033[38;5;240m' + format_ + '\033[0m',
      logging.WARNING: '\033[38;5;226m' + format_ + '\033[0m',
      logging.ERROR: '\033[38;5;196m' + format_ + '\033[0m',
      logging.CRITICAL: '\033[1;31m' + format_ + '\033[0m'
  }

  def format(self, record):
    if record.levelno in self.FORMATS:  # only add color codes if logging to console
      formatter = logging.Formatter(self.FORMATS[record.levelno])
    else:
      formatter = logging.Formatter(self.format_)
    return formatter.format(record)

console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())

file_handler = logging.FileHandler(f"logs/{date.today().strftime('%d-%m-%Y')}.log", encoding='utf-8')
file_handler.setFormatter(logging.Formatter(CustomFormatter.format_))

logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%dZ%z %H:%M:%S', handlers=(console_handler, file_handler))
log = logging.getLogger()
