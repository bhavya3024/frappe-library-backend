from sqlalchemy import ARRAY, DateTime, func

from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MembersModel(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, name='first_name')
    middle_name = Column(String, name='middle_name')
    last_name= Column(String, name='last_name')
    email=Column(String, name='email')
    created_at=Column(DateTime, name='created_at', default=func.now())
    updated_at=Column(DateTime, name='updated_at', default=func.now(), onupdate=func.now())

    # def members_model_to_dict(member_instance):
    #     columns = member_instance.__table__.columns.keys()
    #     member_dict = {col: getattr(member_instance, col) for col in columns}
    #     return member_dict
