__author__ = 'PapEr'

import requests
import bs4
import logging
import re
import time
import datetime
import os

LOGIN_ADDRESS = 'https://leetcode.com/accounts/login/'
HOME_ADDRESS = 'https://leetcode.com/problemset/algorithms/'
LEETCODE_ADDRESS = 'https://leetcode.com'
logging.basicConfig(level=logging.DEBUG)


def login():
    session = requests.session()
    login_page = session.get(LOGIN_ADDRESS)
    login_soup = bs4.BeautifulSoup(login_page.text, 'html.parser')
    login_csrf = login_soup.select('form.form-signin > input')[0]['value']
    login_headers = {'Origin': 'https://leetcode.com',
                     'Referer': 'https://leetcode.com/accounts/login/',
                     'User-Agent': '''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_
                     10_3) AppleWebKit/537.36
                     (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'''
                     }
    session.headers.update(login_headers)
    data = {'login': 'zw.paper@gmail.com', 'password': 'qwer1234',
            'csrfmiddlewaretoken': login_csrf}
    req = session.post(LOGIN_ADDRESS, data)
    if req.status_code == 200:
        logging.debug('login successfully')
        return session, req


def get_front_page(req):
    soup = bs4.BeautifulSoup(req.content, "html.parser")
    # list_problem_all = soup.select('table#problemList > tbody')
    tags_table = soup.find_all('tr')
    list_problems = tags_table[2:]
    problems = []
    premium_problems = []
    for item in list_problems:
        problem = {}
        problem['id'] = item.td.find_next_sibling().contents[0]
        problem['tag'] = item.span['class'][0]
        problem['href'] = item.a['href']
        problem['name'] = item.a.contents[0]
        if item.i:
            premium_problems.append(problem)
        else:
            problems.append(problem)
    return problems, premium_problems


def get_problem_page(session, problem_link):
    response = session.get(problem_link)
    if response.status_code == 200:
        logging.debug('Problem page get.')
        problem_soup = bs4.BeautifulSoup(response.content)
        problem = {}
        problem['title'] = re.match(
            '([\w\s]*)|', problem_soup.title.text).groups()[0].strip()
        problem['description'] = problem_soup.find_all(
            attrs={'name': 'description'})[0]['content']
        return problem


def testing():
    se, res = login()
    list_problems, pre = get_front_page(res)

    os.remove(os.path.expanduser('~') + '/temp/time_check')
    f = open(os.path.expanduser('~') + '/temp/time_check', 'a')
    f.write(str(datetime.datetime.now()) + '\n')
    for i in range(1):
        time_start = time.time()
        for pro_item in list_problems:
            pro = get_problem_page(se, LEETCODE_ADDRESS + pro_item['href'])
            f.write(pro_item['href'] + '\t' + pro['title'] + '\n')
        time_end = time.time()
        f.write(str(time_end - time_start) + '\n\n')

    f.write('premium problems:\n')
    for pre_item in pre:
        f.write(pre_item['name'] + pre_item['href'] + '\n')

    f.close()
