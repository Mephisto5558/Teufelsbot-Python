import logging

logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%dZ%z %H:%M:%S')

class CustomFormatter(logging.Formatter):
  format_ = '%(asctime)s %(module)s#%(lineno)d: %(message)s'

  FORMATS = {
      logging.DEBUG: '\033[38;5;33m' + format_ + '\033[0m',
      logging.INFO: '\033[38;5;240m' + format_ + '\033[0m',
      logging.WARNING: '\033[38;5;226m' + format_ + '\033[0m',
      logging.ERROR: '\033[38;5;196m' + format_ + '\033[0m',
      logging.CRITICAL: '\033[1;31m' + format_ + '\033[0m'
  }

  def format(self, record):
    formatter = logging.Formatter(self.FORMATS.get(record.levelno))
    return formatter.format(record)

logger = logging.getLogger()

console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())
logger.handlers = [console_handler]