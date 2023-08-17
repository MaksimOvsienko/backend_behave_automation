import configparser
import pathlib

from sqlalchemy import create_engine


def get_config():
    config = configparser.ConfigParser()
    p = pathlib.Path(__file__).parent.resolve()
    config.read(f'{p}/properties.ini')
    return config


def get_connection():
    postgres_config = {
        "USERNAME": get_config()['SQL']['USERNAME'],
        "PASSWORD": get_config()['SQL']['PASSWORD'],
        "IP_ADDRESS": get_config()['SQL']['IP_ADDRESS'],
        "PORT": get_config()['SQL']['PORT'],
        "DATABASE_NAME": get_config()['SQL']['DATABASE_NAME']
    }

    try:
        # engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/PythonAutomation', pool_pre_ping=True)
        engine = create_engine(
            'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{IP_ADDRESS}:{PORT}/{DATABASE_NAME}'.format(**postgres_config),
            pool_pre_ping=True
        )
        conn = engine.raw_connection()
        return conn
    except Exception as e:
        print("Connection is fucked. Details: ", e)


def perform_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()
    return row


def get_password():
    return "1234"
