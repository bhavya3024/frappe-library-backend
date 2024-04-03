from sqlalchemy import ARRAY, DateTime, func
from utils.index import ResponseExecption
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class BookMembersDto(BaseModel):
    book_id = int
    member_id = int
    rent_start_date = DateTime
    rent_end_date = DateTime

    def __init__(self):
        if self.rent_start_date >= self.rent_end_date:
            raise ResponseExecption(status=400, message="Rental Start Date should always be before the rental end date")
