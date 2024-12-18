from enum import Enum

class UserRoles(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    
    @classmethod
    def get_permissions(cls) -> None:
        pass