import logging
import sys
from pathlib import Path

LOG_FILE = Path("logs/app.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Консольный обработчик
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# Файловый обработчик
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)

# Настройка корневого логгера
logging.basicConfig(level=logging.INFO, handlers=[console_handler, file_handler])

# Основной логгер
logger = logging.getLogger("app")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
