from flask import Flask, jsonify, request
import pickle
import redis
from database import load_movies
from scipy.sparse import load_npz
import logging
import pickle


app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Redis connection setup
redis_client = redis.StrictRedis(
    host='redis-host',
    port=redis_port,
    password='password',
    decode_responses=False  # Ensure binary responses
)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Load the movie list from PostgreSQL
movies = load_movies()


@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        movie_title = request.args.get('movie')

        # Validate movie title
        if not movie_title:
            return jsonify({"error": "Movie title is required"}), 400

        # Check cache first
        cached_recommendations = redis_client.get(movie_title)
        if cached_recommendations:
            try:
                if isinstance(cached_recommendations, bytes):
                    recommendations = pickle.loads(cached_recommendations)
                else:
                    raise TypeError("Cached data is not in bytes format")

                return jsonify(recommendations=recommendations)
            except pickle.PickleError as e:
                logging.error(f"Error decoding cached recommendations: {e}")
                return jsonify({"error": "Error decoding cached recommendations"}), 500

        # Check if the movie is in the dataset
        if movie_title in movies['title'].values:
            index = movies[movies['title'] == movie_title].index[0]

            # Extract the row of similarities for the given movie
            distances = similarity[index].toarray().flatten()

            # Get indices and sort by similarity score
            distance_with_index = list(enumerate(distances))
            distance_with_index.sort(key=lambda x: x[1], reverse=True)

            recommendations = []
            # Get top 5 similar movies (excluding the queried movie)
            for i in distance_with_index[1:6]:
                recommend_movie = movies.iloc[i[0]].title
                recommendations.append(recommend_movie)

            # Cache the recommendations
            try:
                redis_client.set(movie_title, pickle.dumps(recommendations), ex=86400)
            except pickle.PickleError:
                return jsonify({"error": "Error encoding recommendations for cache"}), 500

            return jsonify(recommendations=recommendations)

        else:
            return jsonify({"error": "Movie not found"}), 404

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True)
