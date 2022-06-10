import requests
from bs4 import BeautifulSoup
import pandas

url = 'https://www.indeed.com/jobs?q=web&l=Texas&start=10&vjk=f13c741454817e27'


def get_total_pages():
    params = {

    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
    }

    # scraping total pages
    total_pages = []

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    pagination = soup.find('ul', 'pagination-list')
    pages = pagination.find_all('li')

    for page in pages:
        total_pages.append(page.text)

    total = int(max(total_pages))
    return total


def get_data():
    params = {

    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    contents = soup.find_all('div', 'slider_container css-11g4k3a eu4oa1w0')

    job_list = []
    base_url = 'https://www.indeed.com/'

    # pick items
    # *title
    # *company name
    # *company location
    # *company link
    # *company salary
    # *job type

    for content in contents:
        title = content.find('h2', 'jobTitle').text.strip()
        company = content.find('span', 'companyName')
        company_name = company.text.strip()
        company_location = content.find('div', 'companyLocation').text.strip()

        try:
            company_link = base_url + company.find('a')['href']
        except:
            company_link = 'Link is not available'

        try:
            company_salary = content.find('span', 'estimated-salary').find('span').text.strip()
        except:
            company_salary = 'none'

        try:
            job_type = content.find('div', 'attribute_snippet').text.strip()
        except:
            job_type = 'none'


def run():
    pass


if __name__ == '__main__':
    get_data()