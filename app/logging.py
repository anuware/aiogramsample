import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    # Изменяем путь к директории логов на "log"
    log_directory = "log"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    logger = logging.getLogger("bot_logger")
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    file_handler = RotatingFileHandler(
        os.path.join(log_directory, "bot.log"),
        maxBytes=5242880,  # 5MB
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger