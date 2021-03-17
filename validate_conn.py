# Imports SF Acct Sign-in Credentials
from sfCredentials import acct
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from sqlalchemy.orm import sessionmaker

# If this program prints a version number (EX: 5.7.6) then the connection to a SF account works

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


# querying
# result = session.query(DataProfile).all()
# for row in result:
#     print(row.dp_id)

newRow = DataProfile(parent_id=1)
session.add(newRow)
session.commit()


try:
    connection = engine.connect()
    
    # simple verification test
    results = connection.execute('select current_version()').fetchone()
    print(results[0])

    # works
    # connection.execute('INSERT INTO data_profile(parent_id) VALUES (0);')   
finally:
    connection.close()
    engine.dispose()