import re
import requests
from bs4 import BeautifulSoup

# Step 1: Create the urls
BASE_URL = "https://www.seek.com.au/"
LISTING_LOCATION_JOB_URL = "https://www.seek.com.au/junior-developer-jobs/in-Melbourne-VIC-3000"

# def addSearchTermsToURL(url:str, searchTerms:list) -> str:
#     return url + "/".join(searchTerms)

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

        

        
links = []
for i in range(1, 2):
    url = addPageNumberToURL(LISTING_LOCATION_JOB_URL, i)
    jobs = getJobLinks(getPageContent(url))
    if len(jobs) <= 0:
        break

    links += jobs
    print("Page " + str(i) + " done")

links = list(set(links))
print(len(links))

print(getJobData(BASE_URL, links[0]))
# getJobData("https://www.seek.com.au/job/68163743?type=standard#sol=49771ce0c397768622365dc367e9d5676b969375", "")


