import sys
import subprocess
import urllib.request
from time import sleep
from multiprocessing import Pool

while True:
    try:
        from bs4 import BeautifulSoup
        break
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', 'beautifulsoup4'])

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
    'postgresql',
    'redis',
    'solr',

    # Frameworks
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
    'spark',
    'spring',
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
        # page = requests.get(source, headers=HEADERS, allow_redirects=False)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
        soup = BeautifulSoup(the_page, "html.parser")
        all_vacancies = soup.find_all("a", class_="bloko-link HH-LinkModifier")
        if all_vacancies:
            # Extract links to vacancy pages and clean them from unnecessary tails.
            for vacancy in all_vacancies:
                link = vacancy.get("href").split("?")[0]
                if link in all_links:
                    pass
                else:
                    all_links.append(link)
            page_num += 1
        else:
            break
    return all_links


def fetch_vacancy_pages(url):
    # Fetch data from vacancy pages.
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
    sleep(0.2)
    soup = BeautifulSoup(the_page, "html.parser")
    description = soup.find(attrs={"data-qa": "vacancy-description"}).text
    # Remove the punctuation except the # and + signs.
    all_data = description.translate(str.maketrans(
        "", "", "!\"$%&'()*,-./:;<=>?@[\\]^_`{|}~"))
    return all_data


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
    p = Pool(20)
    all_data = tuple(p.map(fetch_vacancy_pages, all_links))
    p.terminate()
    p.join()
    process_data(all_data)
