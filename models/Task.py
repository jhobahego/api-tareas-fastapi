from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Task(Base):
    __tablename__ = 'tarea'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")
