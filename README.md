# 🎧 BI & AI Project – Spotify Music Trends Analysis

This Business Intelligence project, completed as part of the Master's in Business Analytics (2024–2025), focuses on analyzing Spotify music trends and showcasing insights through interactive dashboards and a personalized recommendation web app.

## 🚀 Project Goals

* Detect music trends (genres, tempo, popularity, etc.)
* Understand correlations between audio features and commercial success
* Build an optimized relational database for music analytics
* Develop a dynamic Power BI dashboard
* Create a personalized music recommendation web app

## 📚 Methodology: CRISP-DM

The project follows the CRISP-DM framework:

1. **Business Understanding**: Identifying user needs (labels, artists, platforms)
2. **Data Understanding**: Exploratory analysis using Spotify and Kaggle datasets
3. **Data Preparation**: Cleaning, normalization, and PostgreSQL structuring
4. **Modeling**: Correlation studies, KPIs, and a KNN recommendation model
5. **Evaluation**: Interpreting insights with a business perspective
6. **Deployment**: Power BI dashboards + interactive web app

## 🧠 Data Sources

* **Spotify API (Spotipy)**: Audio features (tempo, loudness, energy, danceability, popularity, etc.)
* **Kaggle**: Historical datasets and additional genre info
* **PostgreSQL Database**: Implemented using a constellation schema

## 📈 Key Performance Indicators (KPIs)

* 📊 **Loudness Trends**: Evolution of average song volume
* 🎼 **Emerging Genres**: New styles rising in popularity
* 💃 **Danceability vs Popularity**: Do danceable tracks perform better?
* ⏱ **Tempo Evolution**: Are songs getting faster over time?

## 🔍 Analytical Results

* Strong correlation between energy and loudness
* Lower popularity for highly acoustic tracks
* Dominant genres: pop, dance, hip-hop
* Song length decreasing steadily after 2015

## 📊 Power BI Dashboards

Three interactive dashboards were built to visualize the insights:


> ![Dashboard Spotify](https://github.com/Athenwine/spotify_pi_project/blob/main/dashboard.png?raw=true)

## 🌐 Interactive Web Application

Built with Flask, HTML/CSS/JS, the app features:

* Similar song recommendations
* Playlist generation based on mood (party, chill, etc.)
* Visual comparison of tracks (radar chart)
* Exploration by year or artist
* Clean, responsive, and modern UI

## 🛠 Technical Architecture

* **Backend**: Flask + PostgreSQL + KNN model
* **Frontend**: HTML/CSS + JavaScript + Chart.js
* **REST API**: Smooth communication between layers

## 📁 Repository Structure
```
📦 Spotify_PI
 ┣ 📊 data/
 ┣ 📁 notebooks/
 ┣ 📁 dashboard.png
 ┣ 📄 app.py
 ┣ 📄 requirements.txt
 ┣ 📄 README.md
 ┗ 📁 templates/
```

## 🚀 Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
python app.py
```

---

**Note**: This project was developed as part of the Master's in Business Analytics program (2024–2025).
