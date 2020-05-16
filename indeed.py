import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("div", class_="pagination")
    links = pagination.find_all("a")
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("a").get("title")
    company = html.find("span", class_="company")
    if company:
      company_anchor = company.find("a")
      if company_anchor is not None:
          company = company_anchor.string
      else:
          company = company.string
      company = company.strip()
    else:
      company = None
    location = html.find("div", class_="recJobLoc").get("data-rc-loc")
    job_id = html.get("data-jk")
    return {
        "title":
        title,
        "company":
        company,
        "location":
        location,
        "link":
        f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping indeed page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", class_="jobsearch-SerpJobCard")
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs