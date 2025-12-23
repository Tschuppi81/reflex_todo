import reflex as rx

from sqlmodel import Field
from typing import Optional

class Task(rx.Model, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    state: str  # 'open' | 'in_progress' | 'closed'
