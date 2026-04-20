from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def scrape_indeed(job_title, location):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = f"https://pk.indeed.com/jobs?q={job_title.replace(' ', '+')}&l={location}"
    
    try:
        driver.get(url)
        time.sleep(8) # Indeed takes time to load

        jobs = []
        # Modern Indeed selector for job cards
        cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")

        for card in cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, 'h2.jobTitle span[id^="jobTitle-"]').text
                company = card.find_element(By.CSS_SELECTOR, 'span[data-testid="company-name"]').text
                loc = card.find_element(By.CSS_SELECTOR, 'div[data-testid="text-location"]').text
                try:
                    salary = card.find_element(By.CSS_SELECTOR, 'div.salary-snippet-container').text
                except:
                    salary = "N/A"
                
                jobs.append({"Title": title, "Company": company, "Location": loc, "Salary": salary, "Source": "Indeed", "Category": job_title})
            except:
                continue
        
        driver.quit()
        return pd.DataFrame(jobs)
    except Exception as e:
        driver.quit()
        return pd.DataFrame()