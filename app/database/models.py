from datetime import datetime
from sqlalchemy import ForeignKey, String, BigInteger, DateTime, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    rank: Mapped[str] = mapped_column(String(32), default='Пользователь', nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    last_active: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        Index('idx_tg_id', 'tg_id'),
        Index('idx_username', 'username'),
    )

    def __repr__(self):
        return f"<User(id={self.id}, tg_id={self.tg_id}, username={self.username}, rank={self.rank})>"