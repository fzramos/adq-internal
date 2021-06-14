import subprocess
from config import Config
from snowflake.sqlalchemy import URL as sfURL
import sqlalchemy.engine.url as url
import os
from db_url import create_db_url
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

def main():
    db_setup('snowflake')

def db_setup(db_type='snowflake'):
    if not os.path.isfile('alembic.ini'):
        db_url = create_db_url(db_type)
        simple_url = url.make_url(db_url.split('/PUBLIC')[0]) # only include location and db name
        try:
            create_database(simple_url)
            # try to create database ADQ
        except:
            print('Database ADQ already exists.')
        # if not database_exists(simple_url): # Checks for the first time  
        #     print('is it in!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        #     create_database(simple_url)     # Create new DB    

        # Starting Alembic
        subprocess.run('alembic init alembic'.split(), text=True, check=True)

        # Modify Alembic files with DB information
        with open("alembic.ini","r+") as f:
            data = f.readlines()
            index_line = first_substring(data, 'sqlalchemy.url = ')
            data[index_line] = f'sqlalchemy.url = {db_url}\n'
            f.seek(0)
            f.writelines(data)
        with open("alembic/env.py","r+") as f:
            data = f.readlines()
            index_line = first_substring(data, 'from alembic import context')
            model_import = ['from models import Base\n', 'target_metadata = [Base.metadata]\n']
            if db_type == 'snowflake':
                sf_addition = ['from alembic.ddl.impl import DefaultImpl\n', 'class SnowflakeImpl(DefaultImpl):\n', "    __dialect__ = 'snowflake'\n"]
                model_import += sf_addition        
            data = data[:index_line] + model_import + data[index_line:]

            index_line = first_substring(data, 'target_metadata = None')
            data[index_line] = '#target_metadata = None\n'
            f.seek(0)
            f.writelines(data)
    # Set-up and upload models to database
    subprocess.run(['alembic', 'revision', '--autogenerate', '-m', '“First commit”'], text=True, check=True)
    subprocess.run('alembic upgrade head'.split(), text=True, check=True)
    
def first_substring(strings, substring):
    return next((i for i, string in enumerate(strings) if substring in string), -1)

if __name__ == '__main__':
    main()