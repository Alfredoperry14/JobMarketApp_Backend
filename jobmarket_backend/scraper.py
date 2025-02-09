import time
import random
import re
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from database import SessionLocal, Job

def scrape_jobs():
    url = "https://www.builtinnyc.com/jobs?search=software+engineer"

    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Wait for job cards to load
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-id='job-card']"))
        )
        time.sleep(7)  # Extra wait for JavaScript to finish rendering
    except Exception as e:
        print("Error waiting for job content to load:", e)

    # Simulate scrolling to the bottom to force lazy loading (if any)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # Minor mouse movement to simulate human behavior
    ActionChains(driver).move_by_offset(100, 200).perform()
    time.sleep(random.uniform(2, 5))

    # Get the updated page source and quit the browser
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    # Debug: print snippet of page source to check for job cards
    print("Page source snippet:")
    print(soup.prettify()[:2000])

    # Use a generic selector for job cards
    job_listings = soup.select("div[data-id='job-card']")
    print(f"Found {len(job_listings)} jobs")

    if len(job_listings) == 0:
        print("No jobs found. The website structure may have changed.")
        return

    db = SessionLocal()

    for job in job_listings:
        time.sleep(random.uniform(1, 3))  # Simulate human-like pauses

        # Extract company name
        company = job.find("a", {"data-id": "company-title"})
        company_name = company.get_text(strip=True) if company else "N/A"

        # Extract job title
        job_title = job.find("a", {"data-id": "job-card-title"})
        title = job_title.get_text(strip=True) if job_title else "N/A"

        #Remote/Hybrid
        location_icon = job.find("i", class_=["fa-regular", "fa-location-dot"])
        job_location = "N/A"
        if location_icon:
            parent_div = location_icon.find_parent("div")
            if parent_div:
                next_div = parent_div.find_next_sibling("div")
                if next_div:
                    location_span = next_div.find("span")
                    if location_span:
                        job_location = location_span.get_text(strip=True)
        
        
        # Find the clock icon
        clock_icon = job.find("i", class_=["fa-regular", "fa-clock"])
        post_date_text = "N/A"  # Default value if posting date is not found
        if clock_icon:
            # Get the parent <span> element
            parent_span = clock_icon.find_parent("span")
            if parent_span:
                # Extract all the text within the parent <span>
                post_date_text = parent_span.get_text(strip=True)
                        
        job_level = "N/A"
        for span in job.find_all("span", class_="font-barlow text-gray-04"):
            text = span.get_text(strip=True)
            if "level" in text:
                job_level = text

        avg_salary = None
        salary_text = None
        for span in job.find_all("span", class_="font-barlow text-gray-04"):
            text = span.get_text(strip=True)
            if "Annually" in text and "K" in text:
                salary_text = text
                break

        if salary_text:
            # Try to extract a range like "120K-258K"
            salary_match = re.search(r'(\d+)K-(\d+)K', salary_text)
            if salary_match:
                min_salary = int(salary_match.group(1)) * 1000
                max_salary = int(salary_match.group(2)) * 1000
                avg_salary = (min_salary + max_salary) // 2
            else:
                # Fall back to a single salary figure if a range isn't found
                single_salary_match = re.search(r'(\d+)K', salary_text)
                if single_salary_match:
                    avg_salary = int(single_salary_match.group(1)) * 1000

        print(f"Scraped Job: {title} at {company_name}, Location: {job_location}, "
              f"Posted: {post_date_text}, Level: {job_level}, Salary: {avg_salary}")

        job_entry = Job(
            company=company_name,
            title=title,
            salary=avg_salary,
            location=job_location,
            job_type=job_level,
            post_date=datetime.today().date()
        )
        db.add(job_entry)

    db.commit()
    db.close()
    print("Job scraping complete!")

if __name__ == "__main__":
    scrape_jobs()