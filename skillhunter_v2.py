import re
import random
import asyncio

import aiohttp
from bs4 import BeautifulSoup
from lxml.etree import ParseError, ParserError

HEADERS = {
    "user-agent": [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:71.0) Gecko/20100101 Firefox/71.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    ]
}


TECH = (
    # Languages
    ".NET",
    "NET",
    "assembly",
    "C",
    "C#",
    "C++",
    "CSS",
    "CSS3",
    "D",
    "Delphi",
    "Flixir",
    "F#",
    "Go",
    "Golang",
    "Groovy",
    "ES6",
    "HTML",
    "HTML5",
    "Java",
    "JavaScript",
    "JS",
    "Kotlin",
    "MATLAB",
    "NoSQL",
    "Objective-C",
    "Perl",
    "PHP",
    "Python",
    "Python3",
    "R",
    "Ruby",
    "Rust",
    "Scala",
    "SQL",
    "Swift",
    "TypeScript",
    # Databases
    "Cassandra",
    "Elasticsearch",
    "MariaDB",
    "MongoDB",
    "MySQL",
    "Neo4j",
    "PostgreSQL",
    "Redis",
    "Solr",
    # Frameworks
    "aiohttp",
    "Angular",
    "AngularJS",
    "Ansible",
    "Celery",
    "Chef",
    "Dagger",
    "Dagger2",
    "Django",
    "Docker",
    "docker-compose",
    "Drupal",
    "Falcon",
    "FastAPI",
    "Flask",
    "Hadoop",
    "Kafka",
    "Kubernetes",
    "Laravel",
    "Maven",
    "Memcached",
    "Nameko",
    "Nodejs",
    "Nuxt",
    "Puppet",
    "pytest",
    "RabbitMQ",
    "Rails",
    "React",
    "Reactjs",
    "Redux",
    "Sanic",
    "Spark",
    "Spring",
    "Starlette",
    "Symfony",
    "Terraform",
    "Tomcat",
    "Tornado",
    "unittest",
    "Vue",
    "Vuejs",
    "Yii",
    "Zend",
    # Libraries
    "asyncio",
    "BeautifulSoup",
    "Bootstrap",
    "ExtJS",
    "Hibernate",
    "jQuery",
    "Reras",
    "Matplotlib",
    "NumPY",
    "pandas",
    "PyTorch",
    "scikit",
    "scikit-learn",
    "SciPy",
    "Scrapy",
    "Selenium",
    "TensorFlow",
    "Theano",
    # Concepts
    "Agile",
    "CD",
    "CI",
    "CI/CD",
    "DevOps",
    "GraphQL",
    "Microservice",
    "Microservices",
    "Multithreading",
    "MVC",
    "OOP",
    "RESY",
    "Scrum",
    "SOA",
    "SOAP",
    "SOLID",
    # Other
    "Ajax",
    "Apache",
    "AWS",
    "Azure",
    "Babel",
    "Bash",
    "Bitbucket",
    "Capybara",
    "Circle",
    "CircleCI",
    "CloudLinux",
    "Git",
    "GitHub",
    "GitLab",
    "gulp",
    "Imunify360",
    "Jenkins",
    "JIRA",
    "Less",
    "Linux",
    "Nginx",
    "npm",
    "PWA",
    "PyCharm",
    "RSpec",
    "Sass",
    "shell",
    "SPA",
    "STL",
    "Travis",
    "TravisCI",
    "Unix",
    "Webpack",
    "XML",
    "Yarn",
)


def ask_vacancy():
    # Ask for vacancy to parse.
    raw_query = input("Please, enter the job you wanna check 👉 ")
    query = f'"{raw_query}"'
    return query


async def scan_search_results(query, session):
    # Scan search pages for vacancy links.
    page_num = 0
    all_links = set()
    pattern = re.compile(r"https://hh.ru/vacancy/")
    while True:
        payload = {
            "text": query,
            "page": page_num,
        }
        try:
            async with session.get(
                "https://hh.ru/search/vacancy", params=payload
            ) as resp:
                html = await resp.text()
                soup = BeautifulSoup(html, "lxml")
                all_vacancies = soup.find_all("a", href=pattern)
                len_of_all_links_on_previous_iteration = len(all_links)
                # Extract valid links to vacancy pages and clean their tails.
                new_links = set(
                    vacancy["href"].split("?")[0] for vacancy in all_vacancies
                )
                all_links.update(new_links)
                if len(all_links) > len_of_all_links_on_previous_iteration:
                    page_num += 1
                else:
                    break
        except (ParseError, ParserError):
            print("🚨 Error occurred!")
            break
    return all_links


async def fetch_vacancy_page(link, session):
    async with session.get(link) as resp:
        html = await resp.text()
        soup = BeautifulSoup(html, "lxml")
        try:
            description = soup.find(attrs={"data-qa": "vacancy-description"}).text
        except AttributeError:
            print(f"AttributeError occurred with the following URL: {link}")
            pass
        return description


async def fetch_all_vacancy_pages(all_links, session):
    tasks = []
    for link in all_links:
        task = asyncio.create_task(fetch_vacancy_page(link, session))
        tasks.append(task)
    all_descriptions = await asyncio.gather(*tasks)
    return all_descriptions


def process_vacancy_descriptions(all_descriptions):
    # Extract keywords from the descriptions and count each keyword.
    counts = {}
    for description in all_descriptions:
        # This pattern doesn't identify phrases like "Visual Basic .NET"!
        pattern = r"\w+\S+\w+|[a-zA-Z]+[+|#]+|\S+[a-zA-Z]|\w+"
        separated_words = re.findall(pattern, description.casefold())
        for word in separated_words:

            case_insensitive_counts = (key.casefold() for key in counts)
            case_insensitive_tech = [element.casefold() for element in TECH]

            # Option 1. Rate technologies by frequency.
            if word in case_insensitive_counts and word in case_insensitive_tech:
                position = case_insensitive_tech.index(word)
                counts[TECH[position]] += 1
            elif word not in case_insensitive_counts and word in case_insensitive_tech:
                position = case_insensitive_tech.index(word)
                counts[TECH[position]] = 1
            else:
                pass

            # Option 2. Identify new technologies in the entire list of words.
            # if word in case_insensitive_counts:
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


async def main():
    random_headers = random.choice(HEADERS["user-agent"])
    async with aiohttp.ClientSession(
        headers={"user-agent": random_headers},
    ) as session:
        query = ask_vacancy()
        print("Checking the job...")
        all_links = await scan_search_results(query, session)
        print(f"Here are the number of available jobs: {len(all_links)}")
        all_descriptions = await fetch_all_vacancy_pages(all_links, session)
        counts = process_vacancy_descriptions(all_descriptions)
        show_skills(counts)


if __name__ == "__main__":
    asyncio.run(main())
