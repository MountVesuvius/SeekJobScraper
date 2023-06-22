import re, json, requests
from multiprocessing.pool import ThreadPool as Pool
import nltk
from nltk.tokenize import word_tokenize
import collections

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


def cleanText(text):
    stop_words = set(nltk.corpus.stopwords.words('english'))

    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    joined = ' '.join(filtered_sentence)

    pattern = r'\s[\.,!?;:\’\/]+\s' # Remove punctuation surrounded by spaces
    return re.sub(pattern, ' ', joined)

    return cleaned_text

 

        
if __name__ == "__main__":
    nltk.download('stopwords')
    # searches = addSearchTermsToURL(BASE_URL, 'searchParams.json')

    # # Job Collection
    # pool = Pool(len(searches))
    # jobs = {}
    # for search in searches:
    #     pool.apply_async(worker, (search, ITERATION_LIMIT, jobs))

    # pool.close()
    # pool.join()
    # with open('unique_jobs.json', 'w') as f:
        # json.dump(jobs, f, indent=4)

    # Job Data Collection
    with open('unique_jobs.json', 'r') as f:
        jobs = json.load(f)

    urls = [i for i in jobs]
    text = getJobData(BASE_URL, jobs[urls[0]][0])['jobBody']
    cleaned = cleanText(text.lower())
    frequency = collections.Counter(word_tokenize(cleaned))
    print(frequency)


    # a = [set(i.split(' ')) for i in text.split('. ')]
    # print(a)