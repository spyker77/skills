# Try to replace slow lists to more performant collections.deque

import requests

import sys
import random
import subprocess
from time import sleep
from multiprocessing import Pool

# If [SSL: CERTIFICATE_VERIFY_FAILED] occurs, then enable the following 2 lines.
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

while True:
    try:
        from bs4 import BeautifulSoup
        break
    except ImportError:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', 'beautifulsoup4'])


HEADERS = {
    "user-agent": [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    ]}
TECH = (
    # Languages
    '.net',
    'net',
    'assembly',
    'c',
    'c#',
    'c++',
    'css',
    'css3',
    'd',
    'delphi',
    'elixir',
    'f#',
    'go',
    'golang',
    'groovy',
    'es6',
    'html',
    'html5',
    'java',
    'javascript',
    'js',
    'kotlin',
    'matlab',
    'nosql',
    'objective-c',
    'perl',
    'php',
    'python',
    'python3',
    'r',
    'ruby',
    'rust',
    'scala',
    'sql',
    'swift',
    'typescript',

    # Databases
    'cassandra',
    'elasticsearch',
    'mariadb',
    'mongodb',
    'mysql',
    'neo4j',
    'postgresql',
    'redis',
    'solr',

    # Frameworks
    'aiohttp',
    'angular',
    'angularjs',
    'celery',
    'dagger',
    'dagger2',
    'django',
    'docker',
    'docker-compose',
    'drupal',
    'falcon',
    'fastapi',
    'flask',
    'hadoop',
    'kafka',
    'kubernetes',
    'laravel',
    'maven',
    'memcached',
    'nameko',
    'nodejs',
    'nuxt',
    'pytest',
    'rabbitmq',
    'rails',
    'react',
    'reactjs',
    'redux',
    'sanic',
    'spark',
    'spring',
    'starlette',
    'symfony',
    'tomcat',
    'tornado',
    'unittest',
    'vue',
    'vuejs',
    'yii',
    'zend',

    # Libraries
    'beautifulsoup',
    'bootstrap',
    'extjs',
    'hibernate',
    'jquery',
    'keras',
    'matplotlib',
    'numpy',
    'pandas',
    'pytorch',
    'scikit',
    'scikit-learn',
    'scipy',
    'scrapy',
    'selenium',
    'tensorflow',
    'theano',

    # Concepts
    'agile',
    'cd',
    'ci',
    'ci/cd',
    'devops',
    'graphql',
    'microservice',
    'microservices',
    'multithreading',
    'mvc',
    'oop',
    'rest',
    'scrum',
    'soa',
    'soap',
    'solid',

    # Other
    'ajax',
    'apache',
    'aws',
    'azure',
    'babel',
    'bash',
    'bitbucket',
    'capybara',
    'circleci',
    'cloudlinux',
    'git',
    'github',
    'gitlab',
    'gulp',
    'imunify360',
    'jenkins',
    'jira',
    'less',
    'linux',
    'nginx',
    'npm',
    'pwa',
    'pycharm',
    'rspec',
    'sass',
    'shell',
    'spa',
    'stl',
    'travis',
    'unix',
    'webpack',
    'xml',
    'yarn',
)


def ask_vacancy():
    # Ask for vacancy to parse.
    raw_query = input("Please, put the vacancy you wanna check 👉  ").replace(
        "+", "%2B").replace(" ", "+").replace("#", "%23")
    query = f"\"{raw_query}\""
    return query


def scan_search_results(query):
    # Scan search pages for vacancy links.
    all_links = []
    page_num = 0
    while True:
        url = "https://hh.ru/search/vacancy?text=" + \
            query + f"&page={page_num}"
        sleep(0.2)
        random_headers = random.choice(HEADERS["user-agent"])
        req = requests.get(url, headers={"user-agent": random_headers})
        soup = BeautifulSoup(req.text, "html.parser")
        all_vacancies = soup.find_all("a", class_="bloko-link HH-LinkModifier")
        if all_vacancies:
            # Extract valid links to vacancy pages and clean them from unnecessary tails.
            for vacancy in all_vacancies:
                link = vacancy.get("href").split("?")[0]
                if link in all_links or link == "https://hhcdn.ru/click":
                    pass
                else:
                    all_links.append(link)
            page_num += 1
        else:
            break
    return all_links


def fetch_vacancy_pages(url):
    # Fetch data from vacancy pages.
    random_headers = random.choice(HEADERS["user-agent"])
    req = requests.get(url, headers={"user-agent": random_headers})
    sleep(0.2)
    soup = BeautifulSoup(req.text, "html.parser")
    try:
        description = soup.find(attrs={"data-qa": "vacancy-description"}).text
        # Remove the punctuation except the # and + signs.
        all_data = description.translate(str.maketrans(
            "", "", "!\"$%&'()*,-./:;<=>?@[\\]^_`{|}~"))
        return all_data
    except AttributeError:
        print(f"AttributeError occurred with the following URL: {url}")
        pass


def process_data(all_data):
    # Extract and display result data.
    counts = {}
    for data in all_data:
        # Finish cleaning the data by correcting the format of ".net".
        separated_data = (map(lambda d: d.replace(
            "net", ".net"), data.lower().split()))
        for word in separated_data:
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

    # Sort key, value pairs by value in descending order and slice the first 20 items.
    sorted_counts = (
        sorted(counts.items(), key=lambda x: x[1], reverse=True)[:20])
    print(f"🔥  Here are the most demanded knowledge for this position:")
    for pair in sorted_counts:
        print(f"\"{pair[0]}\" – {pair[1]}")


if __name__ == "__main__":
    query = ask_vacancy()
    all_links = scan_search_results(query)
    # print(f"Here are the number of available positions: {len(all_links)}")
    p = Pool(64)
    all_data = tuple(p.map(fetch_vacancy_pages, all_links))
    p.terminate()
    p.join()
    process_data(all_data)
