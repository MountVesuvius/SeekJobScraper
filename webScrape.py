import re, json, requests
from bs4 import BeautifulSoup

def addSearchTermsToURL(url:str, searchTermsFile:str) -> str:
    '''
    Returns a modified URL by adding search terms to it.

    Parameters:
        url (str): The original URL.
        searchTermsFile (str): The file containing search terms.

    Returns:
        str: The modified URL with search terms added.
    '''
    with open('searchParams.json', 'r') as f:
        searchParams = json.load(f)
    scrapingList = []
    # Not currently handling locations
    for term in searchParams['searchTerms']:
        hunt = url + '-'.join(term.split(' ')) + "-jobs/in-Melbourne-VIC-3000"
        scrapingList.append(hunt)
    return scrapingList

def addPageNumberToURL(url:str, pageNum:int) -> str:
    '''
    Returns a modified URL by adding a page number to it.

    Parameters:
        url (str): The original URL.
        pageNum (int): The page number to be added.

    Returns:
        str: The modified URL with the page number added.
    '''
    return url + "?page=" + str(pageNum)

def getPageContent(url:str) -> str:
    '''
    Retrieves the content of a web page as a string.

    Parameters:
        url (str): The URL of the web page.

    Returns:
        str: The content of the web page as a string.
    '''
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    return None

def getJobLinks(pageData:str) -> list:
    '''
    Extracts job links from the page content.

    Parameters:
        pageData (str): The content of a web page.

    Returns:
        list: A list of job links extracted from the page.
    '''
    linkTags = pageData.find_all('a')
    # Using `/job/` as a filter removes advertisement jobs (hard to tell if that's worth it…)
    return [tag.get('href') for tag in linkTags if '/job/' in tag.get('href') ]


def findSalaryData(dataDump:str) -> str:
    '''
    Finds and returns the salary data from a string.

    Parameters:
        dataDump (str): A string containing the data to search for salary information.

    Returns:
        str: The salary data found in the string.
    '''
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
    '''
    Retrieves job data from a specific job link.

    Parameters:
        baseurl (str): The base URL of the website.
        jobLink (str): The specific job link to retrieve data from.

    Returns:
        dict: A dictionary containing job data, including title, employer, work type, salary, and job body.
    '''
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

def getAllJobPostings(url:str, iterationLimit:int=1000) -> set:
    '''
    Retrieves all job postings from a given URL.

    Parameters:
        url (str): The URL of the website to scrape job postings from.
        iterationLimit (int): The maximum number of pages to scrape (default is 1000).

    Returns:
        set: A set of unique job links scraped from the website.
    '''
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
    return set(links)
