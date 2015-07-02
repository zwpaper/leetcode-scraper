__author__ = 'PapEr'

import requests
import bs4
import re
import simplejson as json


ADDRESS = 'https://leetcode.com/tag/linked-list/'

if __name__ == '__main__':
    response = requests.get(ADDRESS)
    soup = bs4.BeautifulSoup(response.text)
    js = soup.findAll('script')
    js = str(js)
    data = re.search(r'(\$\("#question_list"\)\.bootstrapTable\([\s\S]*?data:) ([\s\S]*?)' + r'([\s\S]*?\);)', js)
    data = re.sub(r'[\s\n]*', '', data.group(3))
    data = re.findall(r'{[\s\S]*?}', data)
    print data
    question_list = []
    for d in data:
        d = d[:-2] + '}'
        question_list.append(json.loads(d))

    print len(question_list)
