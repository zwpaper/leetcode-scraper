__author__ = 'PapEr'

import requests
import bs4
import logging

LOGIN_ADDRESS = 'https://leetcode.com/accounts/login/'
HOME_ADDRESS = 'https://leetcode.com/problemset/algorithms/'


logging.basicConfig(level=logging.DEBUG)

def login():
    session = requests.session()
    login_page = session.get(LOGIN_ADDRESS)
    login_soup = bs4.BeautifulSoup(login_page.text)
    login_csrf = login_soup.select('form.form-signin > input')[0]['value']
    login_headers = {'Origin':'https://leetcode.com',
                     'Referer':'https://leetcode.com/accounts/login/',
                     'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
                    }
    session.headers.update(login_headers)
    data = {'login': 'zw.paper@gmail.com', 'password': 'qwer1234', 'csrfmiddlewaretoken': login_csrf}
    req = session.post(LOGIN_ADDRESS, data)
    if req.status_code == 200:
        logging.debug('login successfully')
        return session, req

if __name__ == '__main__':
    request, response = login()
    print response.content
