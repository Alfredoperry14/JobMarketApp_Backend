import requests
from bs4 import BeautifulSoup
from database import SessionLocal, Job
from datetime import datetime

# Function to scrape jobs from Indeed
def scrape_jobs():
    url = "https://www.indeed.com/jobs?q=Software+Engineer&l=New+York%2C+NY&radius=5"  # Update search query as needed
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve jobs")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Find job listings on Indeed
    job_listings = soup.find_all("td", class_="resultContent")

    db = SessionLocal()  # Open database session
    for job in job_listings:
        # Extract Job Title
        job_title = job.find("h2", class_="jobTitle")
        title = job_title.span.text.strip() if job_title else "N/A"

        # Extract Company Name
        company = job.find("span", {"data-testid": "company-name"})
        company_name = company.text.strip() if company else "N/A"

        # Extract Location
        location = job.find("div", {"data-testid": "text-location"})
        job_location = location.text.strip() if location else "N/A"

        # Extract Salary (if available)
        salary_container = job.find("div", class_="metadata salary-snippet-container")
        salary = salary_container.find("div", {"data-testid": "attribute_snippet_testid"}) if salary_container else None
        salary_text = salary.text.strip() if salary else None

        # Convert salary to an integer range if present
        if salary_text and "-" in salary_text:
            min_salary, max_salary = salary_text.replace("$", "").replace(",", "").split(" - ")
            avg_salary = (int(min_salary) + int(max_salary)) // 2
        elif salary_text:
            avg_salary = int(salary_text.replace("$", "").replace(",", ""))
        else:
            avg_salary = None


        # Convert salary to an integer range if present
        if salary_text and "-" in salary_text:
            min_salary, max_salary = salary_text.replace("$", "").replace(",", "").split(" - ")
            avg_salary = (int(min_salary) + int(max_salary)) // 2
        elif salary_text:
            avg_salary = int(salary_text.replace("$", "").replace(",", ""))
        else:
            avg_salary = None

        # Extract Job ID
        job_id_tag = job.find("a", id=lambda x: x and x.startswith("job_"))
        job_id = job_id_tag["id"] if job_id_tag else "N/A"

        # Create a Job object
        job_entry = Job(
            company=company_name,
            title=title,
            salary=avg_salary,
            location=job_location,
            job_type="Full-time",  # Modify as needed
            post_date=datetime.today().date()
        )

        # Add job to the database
        db.add(job_entry)

    db.commit()
    db.close()
    print("Job scraping complete!")

# Run scraper
if __name__ == "__main__":
    scrape_jobs()