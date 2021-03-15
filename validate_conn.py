# for Snowflake Account Credentials
from sfInfo import acct
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

engine = create_engine(URL(
        account = acct['SNOWFLAKE_ACCOUNT'],
        user = acct['SNOWFLAKE_USER'],
        password = acct['SNOWFLAKE_PASSWORD']
    )
)
try:
    connection = engine.connect()
    results = connection.execute('select current_version()').fetchone()
    print(results[0])
finally:
    connection.close()
    engine.dispose()