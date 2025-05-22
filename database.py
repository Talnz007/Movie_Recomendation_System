import psycopg2
import pandas as pd
import logging
import os
from dotenv import load_dotenv
import numpy as np
from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

VECTOR_DIM = 384  # Adjust based on your embedding model


def get_db_connection():
    try:
        conn = psycopg2.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', '6543')),
            dbname=os.getenv('DB_NAME', 'postgres'),
            options=os.getenv('DB_OPTIONS', '-c statement_timeout=0')
        )
        return conn
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        return None


def fetch_all_movie_titles():
    """
    Fetch all movie titles and their IDs.

    Returns:
        list: List of dictionaries with movie titles and IDs.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, title FROM movies;")
            results = cursor.fetchall()
            return [{"id": row[0], "title": row[1]} for row in results]
    except Exception as e:
        logging.error(f"Error fetching all movie titles: {e}")
    finally:
        conn.close()
    return []


def fetch_movie_by_title(title):
    """
    Fetch a movie's embedding by title.

    Args:
        title (str): The movie title.

    Returns:
        dict or None: Movie data including embedding if found.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, title, embedding FROM movies WHERE title = %s;", (title,))
            result = cursor.fetchone()

            if result:
                return {"id": result[0], "title": result[1], "embedding": np.array(result[2])}
    except Exception as e:
        logging.error(f"Error fetching movie by title: {e}")
    finally:
        conn.close()
    return None


def insert_movies_with_vectors(movie_data, vectorizer):
    """
    Inserts movies into the database with calculated embeddings based on overview and genre.

    Args:
        movie_data (list of dict): List of movie dictionaries with 'title', 'overview', and 'genre'.
        vectorizer: Preloaded Hugging Face embedding model.
    """
    # Create db config from environment variables
    db_config = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT', '6543')),
        'dbname': os.getenv('DB_NAME', 'postgres')
    }

    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            for movie in movie_data:
                title = movie['title']
                overview = movie['overview']
                genre = ', '.join(movie['genres'])  # Join genres as a single string
                tags = f"{overview} {genre}"  # Combine overview and genre
                embedding = vectorizer.encode(tags)  # Generate embedding

                query = """
                INSERT INTO movies (title, overview, genres, embedding)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (title) DO NOTHING;
                """
                cur.execute(query, (title, overview, genre, list(embedding)))
        conn.commit()


def fetch_similar_movies(movie_embedding, top_n=5):
    """
    Find the most similar movies based on cosine similarity.

    Args:
        movie_embedding (np.array): The vector embedding of the movie.
        top_n (int): Number of similar movies to return.

    Returns:
        list: List of similar movie titles.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    try:
        with conn.cursor() as cursor:
            query = """
                SELECT title, 1 - (embedding <=> %s) AS similarity
                FROM movies
                ORDER BY similarity DESC
                LIMIT %s;
            """
            cursor.execute(query, (movie_embedding.tolist(), top_n))
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logging.error(f"Error fetching similar movies: {e}")
    finally:
        conn.close()

    return []


def update_embeddings_for_all_tags():
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cursor:
            # Fetch all rows with valid tags
            cursor.execute("""
                SELECT id, tags FROM movies WHERE tags IS NOT NULL AND TRIM(tags) != '';
            """)
            movies_to_update = cursor.fetchall()

            if not movies_to_update:
                logging.info("No movies to update.")
                return

            vectorizer = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            updates = []

            # Wrap the loop with tqdm for a progress bar
            for i, (movie_id, tags) in enumerate(tqdm(movies_to_update, desc="Processing movies")):
                embedding = vectorizer.encode(tags).tolist()
                updates.append((embedding, movie_id))
                if (i + 1) % 10 == 0:  # Log every 10 rows
                    logging.info(f"Processed {i + 1}/{len(movies_to_update)} movies.")

            # Perform the update in bulk for efficiency
            execute_values(cursor, """
                UPDATE movies
                SET embedding = data.embedding
                FROM (VALUES %s) AS data (embedding, id)
                WHERE movies.id = data.id;
            """, updates)
            conn.commit()
            logging.info(f"Successfully updated embeddings for {len(updates)} movies.")

    except Exception as e:
        logging.error(f"Error updating embeddings for all tags: {e}")
    finally:
        conn.close()