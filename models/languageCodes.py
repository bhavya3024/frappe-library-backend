from sqlalchemy import Column, Integer, String, DateTime, func

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LanguageCodeModel(Base):
    __tablename__ = 'language_codes'
    id = Column(Integer, primary_key=True)
    language_code = Column(String, name='language_code')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
