from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Sequence, DateTime, ForeignKey
import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata

class DataProfile(Base):
    __tablename__ = "data_profile"
    # dp_id_seq = Sequence("dp_id_seq")
    # dp_id = Column(Integer, dp_id_seq,  server_default=dp_id_seq.next_value(), primary_key=True)
    dp_id = Column(Integer, Sequence("DP_ID_SEQ"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # relationships
    column_id = relationship('ColumnProfile', backref='dp', lazy = True)
    # parent_id = relationship('Parent', backref='owner', lazy = True)

class ColumnProfile(Base):
    __tablename__ = "column_profile"
    cp_id = Column(Integer, Sequence("cp_id_seq"), primary_key=True)
    # , server_default=cp_id_seq.next_value()
    dp_id = Column(Integer, ForeignKey("data_profile.dp_id"), nullable=False)
    column_name = Column(String(100))
    type_id = Column(Integer, ForeignKey("data_type.type_id"), nullable=False)
    value_count = Column(Integer)
    missing = Column(Integer)
    percent_missing = Column(Float)
    unique_count = Column(Integer)
    max_length = Column(Integer)
    min_length = Column(Integer)
    avg = Column(Float)
    stdev = Column(Float)
    minimum = Column(Float)
    perc25 = Column(Float)
    perc50 = Column(Float)
    perc75 = Column(Float)
    maximum = Column(Float)
    
class DataType(Base):
    __tablename__ = "data_type"
    type_id = Column(Integer, Sequence("type_id_seq"), primary_key=True)
    name = Column(String(8))

    # relationships
    # column_p_id = relationship('ColumnProfile', backref='type', lazy = True)
    

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    acct_number = Column(Integer)

    # relationships
    dp_id = relationship('DataProfile', backref='owner', lazy = True)

# class Parent(Base):
#     __tablename__ = "parent"
#     parent_id = Column(Integer, Sequence('parent_id_seq'), primary_key=True)
#     owner_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    
#     # relationships
#     dp_id = relationship('DataProfile', backref='parent_table', lazy = True)
