# Movie Recommendation System

Welcome to the Movie Recommendation System repository! This project leverages advanced data processing and machine learning techniques to provide personalized movie recommendations to users. Whether you're a film enthusiast looking for your next favorite movie or a developer interested in recommendation systems, this project has something for you.

## Features

- **Personalized Recommendations:** Utilizes collaborative filtering and content-based filtering to provide tailored movie recommendations.
- **Movie Information:** Displays detailed information about each recommended movie, including title, genre, and synopsis.
- **Interactive Interface:** An easy-to-use web interface built with Streamlit, allowing users to interact with the recommendation system seamlessly.
- **Real-time Poster Updates:** Randomly changes movie posters on each page refresh to keep the user experience dynamic and engaging.

## How It Works

1. **Data Collection:** Collects movie data from a comprehensive movie dataset, including user ratings and movie metadata.
2. **Data Preprocessing:** Cleans and preprocesses the data to make it suitable for training machine learning models.
3. **Model Training:** Trains collaborative filtering and content-based filtering models to predict user preferences.
4. **Recommendation Generation:** Generates personalized movie recommendations based on user input and model predictions.
5. **Web Interface:** Provides an interactive web interface using Streamlit, where users can get movie recommendations and see dynamic movie posters.

## Installation

To get started with the Movie Recommendation System, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/movie-recommendation-system.git
    cd movie-recommendation-system
    ```

2. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Streamlit app:**
    ```bash
    streamlit run main.py
    ```

## Usage

- **Getting Recommendations:** Simply enter your favorite movies in the input field, and the system will recommend movies based on your preferences.
- **Dynamic Posters:** Refresh the page to see a new set of random movie posters.
- **Explore Movie Details:** Click on a recommended movie to see detailed information about it.


## Technologies Used

- **Python:** For data processing and model training.
- **Streamlit:** For building the interactive web interface.
- **Scikit-Learn:** For implementing machine learning models.
- **Pandas & Numpy:** For data manipulation and numerical computations.

## Contributing

Contributions are welcome! If you have any ideas or improvements, feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
