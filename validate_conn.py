# Imports SF Acct Sign-in Credentials
from sfCredentials import acct
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Float, Sequence, MetaData, Table, DateTime, ForeignKey
import datetime

# If this program prints a version number (EX: 5.7.6) then the connection to a SF account works
Base = declarative_base()

engine = create_engine(URL(
        account = acct['SNOWFLAKE_ACCOUNT'],
        user = acct['SNOWFLAKE_USER'],
        password = acct['SNOWFLAKE_PASSWORD'],
        database = 'ADQ',
        schema = 'PUBLIC',
        warehouse = 'COMPUTE_WH',
        role='SYSADMIN'
    )
)

session = sessionmaker(bind=engine)()
connection = engine.connect()
# META_DATA = MetaData(bind=connection)

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

# querying
# result = session.query(DataProfile).all()
# for row in result:
#     print(row.dp_id)

newRow = DataProfile(parent_id=1)
session.add(newRow)
session.commit()


try:
    # connection = engine.connect()
    
    # simple verification test
    results = connection.execute('select current_version()').fetchone()
    print(results[0])

    # works
    # connection.execute('INSERT INTO data_profile(parent_id) VALUES (0);')
    
finally:
    connection.close()
    engine.dispose()