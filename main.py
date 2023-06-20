# Step 1: Create the urls

def addSearchTermsToURL(url:str, searchTermsFile:str) -> str:
    with open('searchParams.json', 'r') as f:
        searchParams = json.load(f)
    scrapingList = []
    # Not currently handling locations
    for term in searchParams['searchTerms']:
        hunt = url + '-'.join(term.split(' ')) + "-jobs/in-Melbourne-VIC-3000"
        scrapingList.append(hunt)
    return scrapingList

def addPageNumberToURL(url:str, pageNum:int) -> str:
    return url + "?page=" + str(pageNum)

# Step 2: Make page requests
def getPageContent(url:str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    return None

# Step 3: Get job links from page
def getJobLinks(pageData:str) -> list:
    linkTags = pageData.find_all('a')
    # Using `/job/` as a filter removes advertisement jobs (hard to tell if that's worth it…)
    return [tag.get('href') for tag in linkTags if '/job/' in tag.get('href') ]


# Step 4: Get job data from job links
def findSalaryData(dataDump:str) -> str:
    if re.search(r'\$\d+', dataDump):
        # Find the section with salary data
        match = re.search(r'[^°]*\$\d+[^°]*', dataDump)
        if match:
            # Extract the salary information
            salary_data = match.group()
            salary_list = salary_data.split('°')
            salary_list = ''.join([salary.strip() for salary in salary_list])
            return salary_list
    else:
        return None

def getJobData(baseurl:str, jobLink:str) -> dict:
    content = getPageContent(baseurl + jobLink)
    if content:
        spanDump = ""
        for span in content.find_all('span'):
            spanDump += span.text.strip() + "°"

        return {
            'title': content.find('h1').text.strip(),
            'employer': content.find('span', {'data-automation': 'advertiser-name'}).text.strip(),
            'workType': content.find('span', {'data-automation': 'job-detail-work-type'}).text.strip(),
            'salary': findSalaryData(spanDump),
            'jobBody': content.find('div', {'data-automation': 'jobAdDetails'}).text.strip(),
        }
    return None

def getAllJobPostings(url:str, iterationLimit:int=1000) -> list:
    links = []
    for i in range(iterationLimit):
        page = addPageNumberToURL(url, i)
        jobs = getJobLinks(getPageContent(page))
        if len(jobs) <= 0:
            break

        print("Jobs scraped from page " + str(i) + ": " + str(len(jobs)))
        links += jobs
    print("Total jobs scraped: " + str(len(links)))
    print()
    return list(set(links))

import re, json, requests
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool as Pool
        
ITERATION_LIMIT = 1000
BASE_URL = "https://www.seek.com.au/"

LISTING_LOCATION_JOB_URL = "https://www.seek.com.au/junior-developer-jobs/in-Melbourne-VIC-3000"

def worker(url, iterationLimit, jobs):
    jobs[url] = getAllJobPostings(url, iterationLimit)
        
if __name__ == "__main__":
    searches = addSearchTermsToURL(BASE_URL, 'searchParams.json')

    pool = Pool(len(searches))
    jobs = {}
    for search in searches:
        pool.apply_async(worker, (search, ITERATION_LIMIT, jobs))
    
    pool.close()
    pool.join()

    with open('job_links.json', 'w') as f:
        json.dump(jobs, f)

    # jobs = getAllJobPostings(searches[0], ITERATION_LIMIT)

   
    # print("Number of Jobs found:", len(jobs))

    # print({
    #     'id': jobs[0],
    #     'data': getJobData(BASE_URL, jobs[0])
    # })
