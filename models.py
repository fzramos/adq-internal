from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Sequence, DateTime, ForeignKey
import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class DataProfile(Base):
    __tablename__ = "data_profile"
    dp_id = Column(Integer, Sequence('dp_id_seq'), primary_key=True)
    parent_id = Column(Integer, default = 0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # relationships
    column_id = relationship('ColumnProfile', backref='dp', lazy = True)

class ColumnProfile(Base):
    __tablename__ = "column_profile"
    cp_id = Column(Integer, Sequence('cp_id_seq'), primary_key=True)
    dp_id = Column(Integer, ForeignKey("data_profile.dp_id"), nullable=False)
    column_name = Column(String(100))
    data_type = Column(String(100))
    count = Column(Integer)
    missing = Column(Integer)
    percent_missing = Column(Float)
    unique_count = Column(Integer)
    max_length = Column(Integer)
    min_length = Column(Integer)
    mean = Column(Float)
    std = Column(Float)
    min = Column(Float)
    perc25 = Column(Float)
    perc50 = Column(Float)
    perc75 = Column(Float)
    max = Column(Float)