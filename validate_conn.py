# Imports SF Acct Sign-in Credentials
from sfCredentials import acct
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

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

try:
    connection = engine.connect()
    
    # simple verification test
    results = connection.execute('select current_version()').fetchone()
    print(results[0])

finally:
    connection.close()
    engine.dispose()