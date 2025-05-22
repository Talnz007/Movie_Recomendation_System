from flask import Flask, request, jsonify
from database import fetch_movie_by_title, fetch_similar_movies
import redis
import pickle
import logging
import os
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

# Redis Setup (Commented out for now, but using env vars)
# redis_client = redis.StrictRedis(
#     host=os.getenv("REDIS_HOST"),
#     port=int(os.getenv("REDIS_PORT", "6379")),
#     password=os.getenv("REDIS_PASSWORD"),
#     decode_responses=False
# )

# CACHE_EXPIRY = 86400  # Cache for 24 hours

@app.route('/recommend', methods=['GET'])
def recommend():
    """
    Recommend similar movies based on the given movie title.
    """
    movie_title = request.args.get('movie')
    if not movie_title:
        return jsonify({"error": "Movie title is required"}), 400

    cache_key = f"recommendations:{movie_title.lower()}"
    # cached_recommendations = redis_client.get(cache_key)

    # if cached_recommendations:
    #     recommendations = pickle.loads(cached_recommendations)
    #     return jsonify({"recommendations": recommendations})

    movie_data = fetch_movie_by_title(movie_title)
    if not movie_data:
        return jsonify({"error": "Movie not found"}), 404

    similar_movies = fetch_similar_movies(movie_data["embedding"])
    # redis_client.set(cache_key, pickle.dumps(similar_movies), ex=CACHE_EXPIRY)

    return jsonify({"recommendations": similar_movies})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)