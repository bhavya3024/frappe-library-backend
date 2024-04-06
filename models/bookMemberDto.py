from sqlalchemy import ARRAY, DateTime, func
from utils.index import ResponseExecption
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

Base = declarative_base()

class BookMembersDto(BaseModel):
    book_id: int
    member_id: int
    rent_start_date: datetime
    rent_end_date: datetime
