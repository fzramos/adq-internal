import subprocess
from config import Config
from snowflake.sqlalchemy import URL as sfURL
import sqlalchemy.engine.url as url
import os
from db_url import create_db_url
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import glob
from sqlalchemy.orm import sessionmaker
from models import DataType, User

def main():
    db_setup('snowflake')

def db_setup(db_type='snowflake'):
    if not os.path.isfile('alembic.ini'):
        db_url = create_db_url(db_type)
        # todo 
        if db_type in ['snowflake', 'postgres']:
            simple_url = url.make_url(db_url.split('/PUBLIC')[0]) # only include location and db name
        try:
            if db_type in ['snowflake', 'postgres']:
                create_database(simple_url)
            else:
                create_database(db_url)
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
    # Creation of sequences for table indeces
    if db_type in ['snowflake', 'postgres']:
        commit_dir = os.path.dirname(os.path.realpath(__file__)) + "\\alembic\\versions\\*_first_commit.py"
        commit_filepath = glob.glob(commit_dir)[0]
        with open(commit_filepath, encoding='utf-8', errors='ignore', mode="r+") as f:
            data = f.readlines()
            import_index = first_substring(data, 'import sqlalchemy as sa') + 1
            upgrade_index = first_substring(data, 'def upgrade():') + 1
            seq_import = ['from sqlalchemy.schema import Sequence, CreateSequence\n']
            seq_creation = [
                "    op.execute(CreateSequence(Sequence('TYPE_ID_SEQ')))\n",
                "    op.execute(CreateSequence(Sequence('CP_ID_SEQ')))\n",
                "    op.execute(CreateSequence(Sequence('DP_ID_SEQ')))\n",
                "    op.execute(CreateSequence(Sequence('USER_ID_SEQ')))\n"
            ]
            data = data[:import_index] + seq_import \
                + data[import_index:upgrade_index] + seq_creation + data[upgrade_index:]

            f.seek(0)
            f.writelines(data)
    
    subprocess.run('alembic upgrade head'.split(), text=True, check=True)

    # TODO Upload initial data types and user 0 in user table
    
def first_substring(strings, substring):
    return next((i for i, string in enumerate(strings) if substring in string), -1)

def inital_table_inserts(db_type):
    """
        Inserts the four possible data types into the data_type table and 
        inserts user 0 into the user table
        in user table
    """
    engine = create_engine(create_db_url(db_type))

    session = sessionmaker(bind=engine)()

    try:
        # Creating a new data profile row in the data_profile table
        newProfile = DataProfile(user_id = user_id)
        # Note, newProfile dp_id isn't created until commited since SF creates the value on insert
        session.add(newProfile)

        session.commit()
        
        # Adding data profile rows to column_profile table with a new column of dp_id
        # so rows are related by their new data profile id 
        dp_df["dp_id"] = newProfile.dp_id
        dp_df.to_sql('column_profile', engine, if_exists='append', index=False)
        print("Data profile uploaded sucessfully.")
    finally:
        # connection.close()
        engine.dispose()

if __name__ == '__main__':
    main()