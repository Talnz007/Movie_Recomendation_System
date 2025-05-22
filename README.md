# Movie Recommendation System

![Movie Recommendation](https://img.shields.io/badge/Movie-Recommendation-blue)
![Python](https://img.shields.io/badge/Python-3.8+-success)
![Supabase](https://img.shields.io/badge/Supabase-pgvector-orange)


A machine learning-powered movie recommendation system built with Python, leveraging vector embeddings (pgvector) on Supabase for scalable, fast, and personalized suggestions. Now featuring a "Watch" button for instant movie viewing!

---

## 🚀 Features

- **AI-Powered Recommendations:** Personalized movie suggestions using vector similarity search.
- **Watch Movies Directly:** Instantly stream recommended movies with the new watch feature.
- **Massive Movie Database:** Millions of movies with metadata and embeddings.
- **Blazing Fast:** Uses pgvector for high-performance similarity queries.
- **Modern Stack:** Python backend, PostgreSQL (pgvector), Supabase, Streamlit/React frontend.

---

## 🏗️ Tech Stack

- **Backend:** Python, Flask
- **Database:** PostgreSQL + pgvector (on Supabase)
- **Data:** TMDB API for movie metadata
- **Frontend:** Streamlit, Svelte, or React components
- **Other:** Docker (optional), Redis (optional for caching)

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Talnz007/Movie_Recomendation_System.git
cd Movie_Recomendation_System
```

### 2. Setup Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy and edit the `.env.example` file:

```bash
cp .env.example .env
```

Fill in your database and TMDB API credentials in `.env`.

### 5. Run the Application

```bash
python main.py
```

Or, if you have a frontend:

```bash
streamlit run app.py
```

---

## 🔑 Environment Variables

Edit `.env` as follows:

```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=6543
DB_NAME=your_db_name
DB_OPTIONS=-c statement_timeout=0

TMDB_API_KEY=your_tmdb_api_key
```

---

## 🎬 How to Use

1. **Start the app:** Run the backend and frontend as above.
2. **Search for a movie:** Enter a movie you like.
3. **Get recommendations:** The system finds similar movies using vector similarity search.
4. **Watch a movie:** Click the "Watch" button to stream a recommended title.

**OR JUST GO TO [This Link](https://recommenders.streamlit.app/)**
---

## 🧠 How It Works

- **Embeddings:** Each movie is represented as a vector (embedding) in a high-dimensional space.
- **Vector Search:** When you select a movie, the app finds other movies with similar embeddings using pgvector.
- **Supabase:** Provides scalable, cloud-hosted PostgreSQL with vector support.
- **Integrated Watching:** Watch workflow connects you to available streaming sources.

---

## 📂 Project Structure

```
Movie_Recomendation_System/
├── api/                  # API backend code
├── frontend/             # Frontend UI code
├── database.py           # Database logic
├── main.py               # Main app logic
├── app.py                # App entry point for Streamlit
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment config
├── .gitignore
└── README.md
```

---

## 🛡️ Security & Best Practices

- **Never commit your `.env` file** (it’s in .gitignore).
- Update `requirements.txt` regularly for security.
- Check [GitHub Security Alerts](https://github.com/Talnz007/Movie_Recomendation_System/security/dependabot) for vulnerabilities.

---

## 🤝 Contributing

1. Fork this repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📈 Future Plans

- Collaborative filtering and hybrid models
- User profiles and login
- Advanced analytics and rating system
- Improved streaming provider integration

---

## 📄 License

This project is licensed under the MIT License.

---

## 📬 Contact

Maintained by [Talha Niazi](mailto:Talhaniazai007@gmail.com)

Project URL: [https://github.com/Talnz007/Movie_Recomendation_System](https://github.com/Talnz007/Movie_Recomendation_System)
