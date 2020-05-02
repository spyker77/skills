These scripts was designed to help future newcomers to the programming world quickly identify the most demanded skills and save a ton of time prioritizing what to learn first.

# 🐌 skillhunter_v1
Originally, this was implemented with familiar at the moment Requests + BeautifulSoup.
Due to slow building of the searched pages and consequently appeared errors Selenium webdriver added as middleware on some steps.
Later on, multiprocessing was added as an attempt to optimize the speed of parsing.

# 🚀 skillhunter_v2
This is a continuation of the original idea, only this time based on aiohttp + asyncio to further optimize speed and reduce hardware requirements. For example, the execution time of the query `frontend developer` took 147 secs and 324 secs for v2 and v1 respectively.

# Coming soon...
Hopefully, this will grow into a full-featured Django project. Potentially, hard-coded skills can be replaced by NLP, and the use of this service can be expanded beyond programming.
