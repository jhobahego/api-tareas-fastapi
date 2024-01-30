from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_super_user = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="user")
