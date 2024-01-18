from sqlalchemy import Column, Text, UUID, Enum
from app.db.session import Base


class Sound(Base):
    __tablename__ = "multimedia"

    id = Column(UUID(as_uuid=True), primary_key=True)
    work_id = Column(UUID(as_uuid=True))
    type = Column(Text)
    description = Column(Text)
    tag = Column(
        Enum(
            "ambiental",
            "animal",
            "musica",
            name="sound-category",
        ),
    )
    source = Column(Text)
    copyright = Column(Text)
    reference = Column(Text)
    author_id = Column(UUID(as_uuid=True))
    publication_id = Column(UUID(as_uuid=True))