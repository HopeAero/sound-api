from sqlalchemy import Column, Date, Text, ARRAY, UUID, Enum as SQLAlchemyEnum
from enum import Enum as PythonEnum

from app.db.session import Base

class GenderEnum(PythonEnum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'

class Author(Base):
    __tablename__ = 'authors'

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(Text)
    pseudonim = Column(Text)
    birth_date = Column(Date)
    death_date = Column(Date)
    gender = Column(SQLAlchemyEnum(GenderEnum, name="gender_enum"))
    parents = Column(ARRAY(Text()))
    children = Column(ARRAY(Text()))
    siblings = Column(ARRAY(Text()))