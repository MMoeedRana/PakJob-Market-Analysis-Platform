# 📊 Job Market Analysis System

A comprehensive, real-time job market analysis dashboard that scrapes job data, processes it using Python, and visualizes trends through an interactive Streamlit interface.

## 🚀 Key Features
* **Automated Scraping:** Uses **Selenium** to fetch latest job postings from major platforms.
* **Data Processing:** Leveraging **Pandas** and **NumPy** for cleaning and analyzing market data.
* **Interactive Dashboard:** Built with **Streamlit** for real-time filtering and insights.
* **Professional Visuals:** Dynamic charts using **Seaborn**, **Matplotlib**, and **Plotly**.
* **Robust Backend:** Ready for scaling with **Django** and **PostgreSQL** integration.

## 🛠️ Tech Stack
- **Language:** Python
- **Scraping:** Selenium, BeautifulSoup4
- **Frontend:** Streamlit
- **Backend:** Django, FastAPI
- **Data Science:** Pandas, NumPy, Seaborn, Matplotlib, Plotly
- **Database:** CSV Files (Upgrade to PostgreSQL in Future)

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/MMoeedRana/PakJob-Market-Analysis-Platform.git](https://github.com/MMoeedRana/PakJob-Market-Analysis-Platform.git)
   cd PakJob-Market-Analysis-Platform

# Create and activate a virtual environment:
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies:
pip install -r requirements.txt

# Create folder name `data` in root:

# Windows (CMD)
mkdir data\raw
mkdir data\processed

# Linux/Mac/Bash
mkdir -p data/raw
mkdir -p data/processed

# Scrape Jobs from (Linkedin, Indeed and Rozee.PK)
python main.py

# Run the Dashboard:
streamlit run app.py