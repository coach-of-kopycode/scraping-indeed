import json
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.indeed.com/jobs?'


def get_total_pages(query, location):
    params = {
        'q': query,
        'l': location,
        'vjk': '455282569a65db72'
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
    }

    # scraping total pages
    total_pages = []

    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    pagination = soup.find('ul', 'pagination-list')
    pages = pagination.findAll('li')

    for page in pages:
        total_pages.append(page.text)
    total = int(max(total_pages))

    return total


def get_data(query, location, start):
    params = {
        'q': query,
        'l': location,
        'start': start,
        'vjk': '455282569a65db72'
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
    }

    # scraping proccess
    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    contents = soup.find_all('table', 'jobCard_mainContent big6_visualChanges')

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

        # sorting data
        data_dict = {
            'title': title,
            'company_name': company_name,
            'company_location': company_location,
            'company_link': company_link,
            'company_salary': company_salary,
            'job_type': job_type
        }

        job_list.append(data_dict)

    return job_list


def generate_file(dataframe, filename, location):
    # create csv & excel
    df = pd.DataFrame(dataframe)
    df.to_csv(f'reports/{filename}_{location}_indeed.csv', index=False)
    df.to_excel(f'reports/{filename}_{location}_indeed.xlsx', index=False)
    print(f'File {filename}.csv and {filename}.xlsx successfully created')


def run():
    query = input('Input query : ')
    location = input('Input location : ')
    total = get_total_pages(query, location)

    counter = 0
    final_result = []
    for page in range(total):
        page += 1
        counter += 10
        final_result += get_data(query, location, counter)
        print('Scraping page: ', page)

    # create directory
    try:
        os.mkdir('reports')
    except FileExistsError:
        pass

    # writing json
    with open(f'reports/{query}_{location}.json', 'w+') as json_data:
        json.dump(final_result, json_data)
        print('JSON created')

    # generate file
    generate_file(final_result, query, location)


if __name__ == '__main__':
    run()