# Seek.com.au Job Scraper
## Description
This is a python webscraping project to scrape job listings from seek.com.au. The project is designed to be run on a daily basis to collect new job listings. It also serves as a learning project for me to improve some webscraping skills, as well as learn some multiprocessing/multi-threading skills.

## Note
I have only just begun working on this project, it is no where near complete. I will update this readme as I progress through the project.

## Usage
The project requires a `searchParams.json` file to be in the root directory. This file contains the search parameters for the job search. The file should be in the following format:

```json
{
    "searchTerms": [
        "Job Title",
    ],
    "locations": [
        "Location Name"
    ]
}
```

---

## Todo
### Better searchParams
searchParams.json should be in the following format:
```json
{
    "keywords": "Data Scientist",
    "location": "Sydney",
    "classification": "Information & Communication Technology",
    "subClassification": "Database Development & Administration",
    "workType": "Full Time",
    "salaryRange": "0-999999",
    "salaryType": "Annual",
    "postingTIme": "Last 14 days"
}
```
