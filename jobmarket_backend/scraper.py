import time
import random
from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from database import SessionLocal, Job

def get_actual_date(post_date_text): 
    """Convert a relative time string into an absolute date."""
    today = datetime.today().date()
    
    if "Today" in post_date_text or "Just now" in post_date_text:
        return today
    elif "Yesterday" in post_date_text:
        return today - timedelta(days=1)
    
    match = re.search(r'(\d+)\s+day', post_date_text, re.IGNORECASE)
    if match:
        days_ago = int(match.group(1))
        return today - timedelta(days=days_ago)
    
    return None

def get_driver():
    """Set up Selenium Chrome WebDriver for EC2"""
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome_user_data")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def scrape_jobs():
    session = SessionLocal()
    driver = get_driver()
    
    try:
        driver.get("https://example.com/jobs")  # Replace with actual job board URL
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "job-card")))
        
        job_elements = driver.find_elements(By.CLASS_NAME, "job-card")
        job_count = 0

        for job_element in job_elements:
            title = job_element.find_element(By.TAG_NAME, "h2").text.strip()
            company = job_element.find_element(By.CLASS_NAME, "company").text.strip()
            location = job_element.find_element(By.CLASS_NAME, "location").text.strip()
            salary = job_element.find_element(By.CLASS_NAME, "salary").text.strip() if job_element.find_elements(By.CLASS_NAME, "salary") else None
            post_date_text = job_element.find_element(By.CLASS_NAME, "date").text.strip()
            post_date = get_actual_date(post_date_text)

            job = Job(
                title=title,
                company=company,
                location=location,
                salary=salary,
                post_date=post_date
            )
            
            session.add(job)
            job_count += 1

            if job_count % 10 == 0:  # Commit every 10 jobs
                session.commit()

        session.commit()  # Final commit for remaining jobs

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()
        session.close()

if __name__ == "__main__":
    scrape_jobs()