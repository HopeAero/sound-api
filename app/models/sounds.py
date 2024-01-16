from sqlalchemy import Boolean, Column, Enum, String, UUID

from app.db.session import Base


class SoundModel(Base):
    __tablename__ = "sounds"

    id = Column(UUID, primary_key=True, index=True)
    category = Column(String, nullable=False)
    sound = Column(String, nullable=False)