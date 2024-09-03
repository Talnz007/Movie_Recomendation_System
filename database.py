import psycopg2
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Database connection details
url = 'https://qdsijfxkqpidkurjjkwb.supabase.co'
USER = 'postgres.qdsijfxkqpidkurjjkwb'
PASSWORD = 'Onvkw6d32uEr3Nr6'
HOST = 'aws-0-ap-south-1.pooler.supabase.com'
PORT = '6543'


def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        return conn
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        return None


def insert_movies(movie_list):
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        with conn.cursor() as cursor:
            for movie in movie_list:
                cursor.execute("""
                    INSERT INTO movies (id, title)
                    VALUES (%s, %s)
                    ON CONFLICT (title) DO NOTHING;
                """, (movie['id'], movie['title']))
        conn.commit()
    except Exception as e:
        logging.error(f"Error inserting movies: {e}")
        conn.rollback()
    finally:
        conn.close()


def load_movies():
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()

    try:
        query = "SELECT id, title FROM movies;"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        logging.error(f"Error loading movies: {e}")
        return pd.DataFrame()
    finally:
        conn.close()
