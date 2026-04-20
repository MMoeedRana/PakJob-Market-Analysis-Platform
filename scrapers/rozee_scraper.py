from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_rozee(job_title):
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Rozee spaces ko handle karne ke liye
    search_query = job_title.replace(' ', '+')
    url = f"https://www.rozee.pk/job/jsearch/q/{search_query}"
    
    try:
        driver.get(url)
        
        # Wait for the job listings container
        wait = WebDriverWait(driver, 20)
        
        # Hum check kar rahe hain ke 'jobt' class wale cards load ho jayein
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.jobt")))
        except:
            print(f"Rozee: No job cards appeared for {job_title}")
            driver.quit()
            return pd.DataFrame()

        jobs = []
        # Image ke mutabiq card class 'jobt float-left' hai
        cards = driver.find_elements(By.CSS_SELECTOR, "div.jobt")

        for card in cards:
            try:
                # 1. Title: h3 ke andar a tag, uske andar bdi
                try:
                    title = card.find_element(By.CSS_SELECTOR, "h3 a bdi").text.strip()
                except:
                    title = card.find_element(By.TAG_NAME, "h3").text.strip()
                
                # 2. Company: div.cname ke andar bdi
                try:
                    company = card.find_element(By.CSS_SELECTOR, "div.cname bdi").text.strip()
                except:
                    company = card.find_element(By.CLASS_NAME, "cname").text.strip()
                
                # 3. Location: div.jloc ya div.jobt.float-left ke andar anchors
                try:
                    # Rozee aksar location ko anchor tags mein bdi ke saath dikhata hai
                    loc_elements = card.find_elements(By.CSS_SELECTOR, "bdi.float-left a")
                    loc = loc_elements[0].text.strip() if loc_elements else "Pakistan"
                except:
                    loc = "N/A"

                # 4. Salary (Optional check based on your screenshot)
                try:
                    salary = card.find_element(By.CLASS_NAME, "sal").text.strip()
                except:
                    salary = "N/A"

                jobs.append({
                    "Title": title, 
                    "Company": company, 
                    "Location": loc, 
                    "Salary": salary, 
                    "Source": "Rozee", 
                    "Category": job_title
                })
            except Exception as e:
                continue

        driver.quit()
        return pd.DataFrame(jobs)
        
    except Exception as e:
        print(f"Rozee Major Error: {e}")
        driver.quit()
        return pd.DataFrame()