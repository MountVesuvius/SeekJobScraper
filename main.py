import re, json, requests
from multiprocessing.pool import ThreadPool as Pool
from webScrape import *
        
ITERATION_LIMIT = 1000

BASE_URL = "https://www.seek.com.au/"
LISTING_LOCATION_JOB_URL = "https://www.seek.com.au/junior-developer-jobs/in-Melbourne-VIC-3000"

def worker(url:str, iterationLimit:int, store:dict) -> None:
    '''
    Async Worker function for multiprocessing.

    Parameters:
        url (str): The URL to scrape.
        iterationLimit (int): The maximum number of pages to scrape.
        store (dict): The dictionary to store the results in.
    
    Returns:
        None
    '''
    jobs = getAllJobPostings(url, iterationLimit)
    for i in store:
        overlap = store[i].intersection(jobs)
        jobs -= overlap
    store[url] = jobs

        
if __name__ == "__main__":
    searches = addSearchTermsToURL(BASE_URL, 'searchParams.json')

    pool = Pool(len(searches))
    jobs = {}
    for search in searches:
        pool.apply_async(worker, (search, ITERATION_LIMIT, jobs))

    pool.close()
    pool.join()

    with open('unique_jobs.json', 'w') as f:
        json.dump(jobs, f, indent=4)