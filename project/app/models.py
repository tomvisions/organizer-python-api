from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class UserBase(SQLModel):
    name: str
    email: str
    user_name: str

class UserId(SQLModel):
    id: int = Field(default=None, nullable=False, primary_key=True)

class UserCreate(UserBase):
    pass

class EventBase(SQLModel):
    name: str
    description: str

class EventCreate(EventBase):
    pass

class UserEventLink(SQLModel, table=True):
    user_id:Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    event_id: Optional[int] = Field(
        default=None, foreign_key="event.id", primary_key=True
    )

class Event(EventBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
   # users: List["User"] = Relationship(back_populates="events", link_model="UserEventLink")

class User(UserBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
   # events: List["Event"] = Relationship(back_populates="users", link_model="UserEventLink")
