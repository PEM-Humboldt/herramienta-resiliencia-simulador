from sqlalchemy import create_engine
import os

def db_connect():

    DB_SYSTEM = os.getenv('DB_SYSTEM')
    DB_ADDRESS = os.getenv('DB_ADDRESS')
    DB_PORT = os.getenv('DB_PORT')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')

    if DB_SYSTEM=='oracle':
        SQL_DRIVER = 'cx_oracle'
        connection_str = ('{dbsystem}+{sqldriver}://{username}:{password}@{ipaddress}:{port}/?service_name={dbname}'.format(dbsystem=DB_SYSTEM,
                                                                                                sqldriver=SQL_DRIVER,
                                                                                                username=DB_USERNAME,
                                                                                                password=DB_PASSWORD,
                                                                                                ipaddress=DB_ADDRESS,
                                                                                                port=DB_PORT,
                                                                                                dbname=DB_NAME))
    else:
        # Do not change this long string that contains the necessary MongoDB login information
        connection_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(dbsystem=DB_SYSTEM,
                                                                                                username=DB_USERNAME,
                                                                                                password=DB_PASSWORD,
                                                                                                ipaddress=DB_ADDRESS,
                                                                                                port=DB_PORT,
                                                                                                dbname=DB_NAME))
    # Create the connection
    cnx = create_engine(connection_str)
    return cnx

def set_query(workspace, module, fields):

    DB_SYSTEM = os.getenv('DB_SYSTEM')

    table_name = f'{workspace}_{module}'
    fields_list = ','.join(fields)

    if DB_SYSTEM=='oracle':
        data_query = f'SELECT {fields_list} FROM {table_name}'
    else:
        data_query = f'SELECT {fields_list} FROM public.{table_name}'

    return data_query