from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

def scrape_linkedin(job_title, location):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = f"https://www.linkedin.com/jobs/search?keywords={job_title.replace(' ', '%20')}&location={location}"
    
    try:
        driver.get(url)
        time.sleep(7)

        # Scroll to load more jobs
        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        jobs = []
        cards = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list > li")

        for card in cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, "h3.base-search-card__title").text.strip()
                company = card.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtitle").text.strip()
                loc = card.find_element(By.CSS_SELECTOR, "span.job-search-card__location").text.strip()
                
                jobs.append({"Title": title, "Company": company, "Location": loc, "Salary": "N/A", "Source": "LinkedIn", "Category": job_title})
            except:
                continue

        driver.quit()
        return pd.DataFrame(jobs)
    except:
        driver.quit()
        return pd.DataFrame()