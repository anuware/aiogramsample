
from enum import Enum

class Ranks(Enum):
    OWNER = "Владелец"
    ADMIN = "Администратор"
    MODERATOR = "Модератор"
    USER = "Пользователь"

RANKS_HIERARCHY = {
    Ranks.OWNER.value: 4,
    Ranks.ADMIN.value: 3,
    Ranks.MODERATOR.value: 2,
    Ranks.USER.value: 1
}