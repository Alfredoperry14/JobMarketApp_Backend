# Job Market App
- Link 
## Overview
This **Job Market App** is a personal project that scrapes job postings from [Builtin NYC](http://builtinnyc.com) and allows users to:
- Track **new software engineering job postings**.
- **Mark jobs as applied** and manage applications.
- View **job statistics** (salary trends, job levels, locations) using **Swift Charts**.

This project was built as a learning experience to explore **iOS development with SwiftUI**, **backend development with FastAPI**, **web scraping**, and **AWS server deployment**.

---
## Features
### 📌 Job Listings (`JobListView`)
- Displays jobs in an **organized** and **sortable** manner.
- Filtering by title, company, location, level, salary, and post date.
- Pagination for browsing through listings efficiently.
- Added a button to see job listings posted within the last 24 hours 
- Learned a lot about **sorting logic** for a clean UI.

### 📊 Job Statistics (`JobStats`)
- Visualizes job market data using **Swift Charts**.
- Shows **average salaries**, **job levels**, and **location distribution**.
- First-time experience with Swift Charts, and found it to be an effective tool for data visualization.

### 🌐 Job Page (`JobPageView`)
- Displays detailed job descriptions within the app.
- Uses **WebKit** to **load job pages** directly in-app instead of opening Safari.
- **Clipboard functionality** to copy job links.
- This feature was particularly exciting because integrating WebKit was **rewarding to see in action**.

---
## Backend Setup
The backend is built using **FastAPI + PostgreSQL** and deployed on an **AWS EC2 Ubuntu server**.

### 🚀 Key Backend Highlights
- **Web Scraping**: Originally tried **Indeed**, but switched to Builtin NYC due to anti-scraping measures.
- **AWS**: It was my first time using AWS,and it was clear there was so much you could do. I want to learn more.
- **Docker**: First time writing a **Dockerfile** to containerize the web scraper and API. I had to do this because I ran into issues with finding the Chromium binary file, was feeling discouraged at times, but Docker made the process so much easier. 
- **Automation**: Initially ran the scraper manually but later **automated** job fetching to run twice a day.

**Backend Repo:** [🔗 Link to Backend Repository](https://github.com/Alfredoperry14/JobMarketApp_FrontEnd)

---
## Technologies Used
### Frontend:
- **SwiftUI** (UI framework)
- **WebKit** (To see the job url within the app)
- **Swift Charts** (For data visualization)

### Backend:
- **FastAPI** (API framework)
- **PostgreSQL** (database)
- **Scrapy** + **BeautifulSoup** (web scraping)
- **Docker** (containerization)
- **AWS EC2 (Ubuntu)** (hosting)

---
## Future Improvements
- **Expand to other locations** on Builtin (e.g., **Boston, Chicago, SF**) and add notifications when the web scraper has added the new jobs.
- Keep refining skills and moving on to new projects:
  - Keep working with async and caches
  - Working with other Apple Frameworks
  - Improving on DS&A

---
## Personal Reflections
- **Sorting data** for `JobListView` was more complex than expected but rewarding.
- **Swift Charts** was an **interesting first-time experience** and is worth using again.
- **Seeing WebKit in action** made the project feel **polished and practical**.
- **Learning AWS, Docker, and automation** felt like a big step forward in backend development.
- Hopefully Move to NYC one day and experience the tech scene firsthand, and just everything the city has to offer.

This was a **great learning project**, and I'm looking forward to **building more!**

<p align="center">
  <img src="https://github.com/user-attachments/assets/4ce3bc9a-567a-4f14-a485-1df17a67de41" width="300">
  <img src="https://github.com/user-attachments/assets/999744e9-5eb9-4578-aa0e-dbcc37759dda" width="300">
  <img src="https://github.com/user-attachments/assets/54d71679-8890-4076-b77a-69a6e2d780bc" width="300">
  <img src =" https://github.com/user-attachments/assets/5cf7e6b5-c56d-4aac-91e7-03905a64f8ba" width = "300">
  <img src = "https://github.com/user-attachments/assets/6a6632b9-ba1f-4770-8360-3ecc147455a8" width = "300">
  <img src = "https://github.com/user-attachments/assets/85754cd5-0416-4449-a5d2-280687ea2b0b" width = "300">
https://github.com/user-attachments/assets/8ab0e690-fd6b-4117-b675-1c9b595e627f

</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/5d8f1791-121b-4573-b568-9bb02a5392d1" width="300">
  <a href="https://github.com/user-attachments/assets/fc35d173-ab03-4423-b18d-61ed82427d64">
  </a>
</p>
(Laggy because the video had to be compressed)


