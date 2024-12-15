# app/const.py
class Ranks:
    OWNER = "Владелец"
    ADMIN = "Администратор"
    MODERATOR = "Модератор"
    USER = "Пользователь"

RANKS_HIERARCHY = {
    Ranks.CREATOR: 4,
    Ranks.ADMIN: 3,
    Ranks.MODERATOR: 2,
    Ranks.USER: 1
}