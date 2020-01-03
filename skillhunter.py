import re
import random
from multiprocessing import Pool
from urllib.parse import urlencode

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import TimeoutException


HEADERS = {
    "user-agent": [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:71.0) Gecko/20100101 Firefox/71.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    ]
}

TECH = (
    # Languages
    ".net",
    "net",
    "assembly",
    "c",
    "c#",
    "c++",
    "css",
    "css3",
    "d",
    "delphi",
    "elixir",
    "f#",
    "go",
    "golang",
    "groovy",
    "es6",
    "html",
    "html5",
    "java",
    "javascript",
    "js",
    "kotlin",
    "matlab",
    "nosql",
    "objective-c",
    "perl",
    "php",
    "python",
    "python3",
    "r",
    "ruby",
    "rust",
    "scala",
    "sql",
    "swift",
    "typescript",
    # Databases
    "cassandra",
    "elasticsearch",
    "mariadb",
    "mongodb",
    "mysql",
    "neo4j",
    "postgresql",
    "redis",
    "solr",
    # Frameworks
    "aiohttp",
    "angular",
    "angularjs",
    "celery",
    "dagger",
    "dagger2",
    "django",
    "docker",
    "docker-compose",
    "drupal",
    "falcon",
    "fastapi",
    "flask",
    "hadoop",
    "kafka",
    "kubernetes",
    "laravel",
    "maven",
    "memcached",
    "nameko",
    "nodejs",
    "nuxt",
    "pytest",
    "rabbitmq",
    "rails",
    "react",
    "reactjs",
    "redux",
    "sanic",
    "spark",
    "spring",
    "starlette",
    "symfony",
    "tomcat",
    "tornado",
    "unittest",
    "vue",
    "vuejs",
    "yii",
    "zend",
    # Libraries
    "beautifulsoup",
    "bootstrap",
    "extjs",
    "hibernate",
    "jquery",
    "keras",
    "matplotlib",
    "numpy",
    "pandas",
    "pytorch",
    "scikit",
    "scikit-learn",
    "scipy",
    "scrapy",
    "selenium",
    "tensorflow",
    "theano",
    # Concepts
    "agile",
    "cd",
    "ci",
    "ci/cd",
    "devops",
    "graphql",
    "microservice",
    "microservices",
    "multithreading",
    "mvc",
    "oop",
    "rest",
    "scrum",
    "soa",
    "soap",
    "solid",
    # Other
    "ajax",
    "apache",
    "aws",
    "azure",
    "babel",
    "bash",
    "bitbucket",
    "capybara",
    "circleci",
    "cloudlinux",
    "git",
    "github",
    "gitlab",
    "gulp",
    "imunify360",
    "jenkins",
    "jira",
    "less",
    "linux",
    "nginx",
    "npm",
    "pwa",
    "pycharm",
    "rspec",
    "sass",
    "shell",
    "spa",
    "stl",
    "travis",
    "unix",
    "webpack",
    "xml",
    "yarn",
)


def initialize_webdriver():
    # Run webdriver with random user-agent and headless mode.
    options = Options()
    options.add_argument("-headless")
    random_headers = random.choice(HEADERS["user-agent"])
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", random_headers)
    driver = webdriver.Firefox(profile, options=options, service_log_path="/dev/null")
    return driver


def ask_vacancy():
    # Ask for vacancy to parse.
    raw_query = input("Please, enter the job you wanna check 👉 ")
    query = f'"{raw_query}"'
    return query


def scan_search_results(query, driver):
    # Scan search pages for vacancy links.
    page_num = 0
    all_links = set()
    while True:
        payload = {
            "text": query,
            "page": page_num,
        }
        try:
            driver.get("https://hh.ru/search/vacancy?" + urlencode(payload))
            WebDriverWait(driver, 0.1).until(
                presence_of_element_located(
                    (By.XPATH, '//a[contains(@href,"https://hh.ru/vacancy")]')
                )
            )
            all_vacancies = driver.find_elements(
                By.XPATH, '//a[contains(@href,"https://hh.ru/vacancy")]'
            )
            # Extract valid links to vacancy pages and clean them from unnecessary tails.
            for vacancy in all_vacancies:
                link = vacancy.get_attribute("href").split("?")[0]
                all_links.add(link)
            page_num += 1
        except TimeoutException:
            # Think of replacing the exception logic with iteration through counting!
            driver.quit()
            break
    return all_links


def fetch_vacancy_pages(link):
    # Fetch data from vacancy pages.
    random_headers = random.choice(HEADERS["user-agent"])
    page = requests.get(link, headers={"user-agent": random_headers})
    soup = BeautifulSoup(page.text, "html.parser")
    try:
        description = soup.find(attrs={"data-qa": "vacancy-description"}).text
        return description
    except AttributeError:
        print(f"AttributeError occurred with the following URL: {link}")
        pass


def process_descriptions(all_descriptions):
    # Extract keywords from the descriptions and count each.
    counts = {}
    for description in all_descriptions:
        pattern = r"\w+\S+\w+|[a-zA-Z]+\S|\S+[a-zA-Z]|\w+"
        separated_words = re.findall(pattern, description.lower())
        # Think of using original formatting of the names for the end result!
        for word in separated_words:
            if word in counts and word in TECH:
                counts[word] += 1
            elif word not in counts and word in TECH:
                counts[word] = 1
            else:
                pass
            # This part is used to identify new technologies in the entire list of words.
            # if word in counts:
            #     counts[word] += 1
            # else:
            #     counts[word] = 1
    return counts


def show_skills(counts):
    # Sort key, value pairs by value in descending order and slice the first 20 items.
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:20]
    print(f"Here are the most demanded skills for this job:")
    for pair in sorted_counts:
        print(f'"{pair[0]}" – {pair[1]}')


if __name__ == "__main__":
    driver = initialize_webdriver()
    query = ask_vacancy()
    print("Checking the job...")
    all_links = scan_search_results(query, driver)
    print(f"Here are the number of available jobs: {len(all_links)}")
    with Pool(64) as p:
        # Show progress bar while fetching previously collected vacancy links.
        all_descriptions = tuple(
            tqdm(
                p.imap_unordered(fetch_vacancy_pages, all_links),
                desc="Processing jobs",
                total=len(all_links),
                bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
            )
        )
    counts = process_descriptions(all_descriptions)
    show_skills(counts)
