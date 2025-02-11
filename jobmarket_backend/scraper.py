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
    
    # Handle common cases
    if "Today" in post_date_text or "Just now" in post_date_text:
        return today
    elif "Yesterday" in post_date_text:
        return today - timedelta(days=1)
    
    # Look for patterns like "2 Days Ago" (or "2 Day Ago") using regex
    match = re.search(r'(\d+)\s+day', post_date_text, re.IGNORECASE)
    if match:
        days_ago = int(match.group(1))
        return today - timedelta(days=days_ago)
    
    # For hours, assume it's still today
    match = re.search(r'(\d+)\s+hour', post_date_text, re.IGNORECASE)
    if match:
        return today  # Still the same day
    
    # Fallback: if no pattern matched, default to today
    return today

def scrape_jobs():
    base_url = "https://www.builtinnyc.com/jobs/dev-engineering?"
    page_number = 1
    
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    db = SessionLocal()

    while True:
        # Construct the URL for the current page
        current_url = f"{base_url}&page={page_number}"
        print(f"Scraping page: {page_number} - {current_url}")
        driver.get(current_url)

        # Wait for job cards to load
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-id='job-card']"))
            )
            time.sleep(7)  # Extra wait for JavaScript to finish rendering
        except Exception as e:
            print("Error waiting for job content to load:", e)
            break

        # Simulate scrolling to the bottom to force lazy loading (if any)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # Minor mouse movement to simulate human behavior
        #ActionChains(driver).move_by_offset(100, 200).perform()
        time.sleep(random.uniform(2, 5))

        # Get the updated page source and parse with BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Find all job cards on this page
        job_listings = soup.select("div[data-id='job-card']")
        print(f"Found {len(job_listings)} jobs on page {page_number}")

        # If no job listings are found, assume we've reached the end.
        if len(job_listings) == 0:
            print("No more jobs found. Ending pagination.")
            break

        for job in job_listings:
            time.sleep(random.uniform(1, 3))  # Simulate human-like pauses

            # Extract company name
            company = job.find("a", {"data-id": "company-title"})
            company_name = company.get_text(strip=True) if company else "N/A"

            # Extract job title and link
            job_title_element = job.find("a", {"data-id": "job-card-title"})
            title = job_title_element.get_text(strip=True) if job_title_element else "N/A"
            job_link = job_title_element.get('href') if job_title_element and job_title_element.has_attr('href') else "N/A"
            # Ensure the link is absolute
            if job_link != "N/A" and not job_link.startswith("http"):
                job_link = "https://www.builtinnyc.com" + job_link

            # Check that we haven't added the job link before
            existing_link = db.query(Job).filter(Job.job_link == job_link).first()
            if existing_link:
                print(f"Job already exists in DB: {job_link}")
                continue  # Skip to the next job in the loop


            # Extract job location (Remote/Hybrid)
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
            
            # Extract post date text
            clock_icon = job.find("i", class_=["fa-regular", "fa-clock"])
            post_date_text = "N/A"
            if clock_icon:
                parent_span = clock_icon.find_parent("span")
                if parent_span:
                    post_date_text = parent_span.get_text(strip=True)

            # Extract job level
            job_level = "N/A"
            for span in job.find_all("span", class_="font-barlow text-gray-04"):
                text = span.get_text(strip=True)
                if "level" in text:
                    job_level = text

            # Extract salary
            avg_salary = None
            salary_text = None
            for span in job.find_all("span", class_="font-barlow text-gray-04"):
                text = span.get_text(strip=True)
                if "Annually" in text and "K" in text:
                    salary_text = text
                    break

            if salary_text:
                salary_match = re.search(r'(\d+)K-(\d+)K', salary_text)
                if salary_match:
                    min_salary = int(salary_match.group(1)) * 1000
                    max_salary = int(salary_match.group(2)) * 1000
                    avg_salary = (min_salary + max_salary) // 2
                else:
                    single_salary_match = re.search(r'(\d+)K', salary_text)
                    if single_salary_match:
                        avg_salary = int(single_salary_match.group(1)) * 1000

            print(f"Scraped Job: {title} at {company_name}, Location: {job_location}, "
                  f"Posted: {post_date_text}, Level: {job_level}, Salary: {avg_salary}, "
                  f"Link: {job_link}")

            actual_post_date = get_actual_date(post_date_text)
            
            # Create job entry with scraped data (including job_link if you later add it to the model)
            job_entry = Job(
                company=company_name,
                title=title,
                salary=avg_salary,
                location=job_location,
                job_type=job_level,
                post_date=actual_post_date,
                job_link=job_link  
            )
            db.add(job_entry)
            job_count += 1
            if job_count % 10 == 0:
                print(f"Committing after processing {job_count} jobs on page {page_number}...")
                session.commit()

        page_number += 1  # Move to the next page

    driver.quit()
    db.commit()
    db.close()
    print("Job scraping complete!")

if __name__ == "__main__":
    scrape_jobs()