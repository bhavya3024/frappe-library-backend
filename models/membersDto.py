from sqlalchemy import ARRAY, DateTime, func

from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional


Base = declarative_base()


class MembersDto(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: str
