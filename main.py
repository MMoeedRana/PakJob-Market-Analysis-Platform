import pandas as pd
import time
import os
import sys

# 1. Path Fix: Taake Python ko 'scrapers' aur 'utils' folders mil sakein
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from scrapers.indeed_scraper import scrape_indeed
    from scrapers.linkedin_scraper import scrape_linkedin
    from scrapers.rozee_scraper import scrape_rozee
    from utils import clean_data
except ImportError as e:
    print(f" Import Error: {e}")
    print("Tip: Check karein ke scrapers folder mein __init__.py file maujood hai.")
    sys.exit(1)

# 2. Settings & Categories
job_categories = [
    "Software Engineer", "Frontend Developer", "Backend Developer",
    "Data Analyst", "Data Scientist", "Artificial Intelligence",
    "Graphic Designer", "Digital Marketing", "Content Writer",
    "Sales Executive", "Project Manager", "HR Manager"
]

all_data = []

print("\n" + "="*50)
print("JOB MARKET ANALYSER - GLOBAL SCRAPER STARTING")
print("="*50)

# Ensure folders exist
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

for category in job_categories:
    print(f"\n PROCESSING CATEGORY: {category}")
    print("-" * 30)
    
    # --- ROZEE.PK SCRAPING ---
    print(f" Scraping Rozee.pk...")
    try:
        df_roz = scrape_rozee(category)
        if df_roz is not None and not df_roz.empty:
            all_data.append(df_roz)
            print(f" Rozee Success: {len(df_roz)} jobs found.")
        else:
            print(f" Rozee: 0 jobs found. (Check browser/selectors)")
    except Exception as e:
        print(f" Rozee Error: {str(e)}")

    # --- INDEED SCRAPING ---
    # Note: Agar sirf Rozee test karna hai toh niche wali lines ko # se comment kar dein
    print(f" Scraping Indeed.com...")
    try:
        df_ind = scrape_indeed(category, "Pakistan")
        if df_ind is not None and not df_ind.empty:
            all_data.append(df_ind)
            print(f" Indeed Success: {len(df_ind)} jobs found.")
        else:
            print(f" Indeed: 0 jobs found.")
    except Exception as e:
        print(f" Indeed Error: {str(e)}")

    # --- LINKEDIN SCRAPING ---
    print(f"📡 Scraping LinkedIn...")
    try:
        df_lin = scrape_linkedin(category, "Pakistan")
        if df_lin is not None and not df_lin.empty:
            all_data.append(df_lin)
            print(f" LinkedIn Success: {len(df_lin)} jobs found.")
        else:
            print(f" LinkedIn: 0 jobs found.")
    except Exception as e:
        print(f"❌ LinkedIn Error: {str(e)}")

    # Anti-blocking delay
    print(f"\n Waiting 10 seconds to avoid IP block...")
    time.sleep(10)

# 3. Data Consolidation & Cleaning
print("\n" + "="*50)
print(" FINALIZING DATA")
print("="*50)

if all_data:
    # Saare dataframes ko combine karein
    final_df = pd.concat(all_data, ignore_index=True)
    
    # Raw backup save karein
    final_df.to_csv("data/raw/jobs_raw_backup.csv", index=False)
    
    # Data Cleaning (from utils.py)
    try:
        cleaned_df = clean_data(final_df)
        
        # Final Processed File
        output_file = "data/processed/all_pakistan_jobs.csv"
        cleaned_df.to_csv(output_file, index=False)
        
        print(f" SUCCESS!")
        print(f" Total Jobs Collected: {len(final_df)}")
        print(f" After Cleaning/Deduplication: {len(cleaned_df)}")
        print(f" File saved at: {output_file}")
        
    except Exception as e:
        print(f" Cleaning Failed: {e}")
        print(" Raw data saved at data/raw/jobs_raw_backup.csv")
else:
    print("\n NO DATA COLLECTED.")