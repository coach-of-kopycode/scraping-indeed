import json
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

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
    print('total data ', len(job_list))

    # make directory
    try:
        os.mkdir('json_result')
        os.mkdir('file_result')
    except FileExistsError:
        pass

    # writing json
    with open('json_result/result.json', 'w+') as json_data:
        json.dump(job_list, json_data)
        print('json created')

    # create csv & excel
    df = pd.DataFrame(job_list)
    df.to_csv('file_result/csv_indeed.csv', index=False)
    df.to_excel('file_result/excel_indeed.xlsx', index=False)
    print('file created')


def run():
    pass


if __name__ == '__main__':
    get_data()