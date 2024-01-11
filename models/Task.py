from sqlalchemy import Column, Integer, String, Boolean

from db import Base


class Task(Base):
    __tablename__ = 'tarea'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    completed = Column(Boolean, default=False)
