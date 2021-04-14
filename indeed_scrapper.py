import requests
from bs4 import BeautifulSoup

LIMIT = 50


def get_last_pages(url) :
  element = 2000

  while(True) :
    result = requests.get(url + f"&start={element}")

    soup = BeautifulSoup(result.text, "html.parser").find("div", {"class" : "pagination"}).find_all('b')
    
    if(soup[-1].string == None) : 
      element -= LIMIT
    else : 
      return int(soup[-1].string)

def extract_job(html) :
  title = html.find("h2", {"class": "title"}).find("a")["title"]

  company = html.find("span", {"class": "company"})
  if company is None : None
  else: 
    company_anchor = company.find("a")
    if company_anchor is not None :
      company = company_anchor.string
    else :
      company = company.string
    company = company.strip()

  location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]

  job_id = html["data-jk"]

  return {'title': title, 
  'company': company, 
  'location': location, 
  'link': f"https://kr.indeed.com/viewjob?jk={job_id}&from=web&vjs=3"}

def extract_jobs(last_page, url):
  jobs = []

  for page in range(last_page) :
    print(f"Scrapping Indeed Page {page + 1}")
    result = requests.get(f"{url}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser").find_all("div", {"class": "jobsearch-SerpJobCard"})
    for s in soup :
      job = extract_job(s)
      jobs.append(job)

  return jobs

def get_jobs(word) :
  url = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and={word}&limit={LIMIT}"
  last_pages = get_last_pages(url)
  jobs = extract_jobs(last_pages, url)

  return jobs