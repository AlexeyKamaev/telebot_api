catch_1 = 'Оценка по условиям'
catch_2 = 'Поиск по ID ЦИАН'
catch_3 = 'ℹ️'

vars_list = list(vars().keys())


catches = sorted(map(eval,filter(lambda x: True if x is not None and 'catch_' in x else False, vars_list)))

urls = ['http://fastapi_backend:8400/','http://127.0.0.1:8000/','http://localhost:8000/','http://158.160.159.119:8400/']

import requests

def get_url():

    global url

    for link in urls:
        try:
            x = requests.get(link)
            text = x.text
            if 'Welcome to CIAN-based' in text:
                url = link
                break
            else:
                url = ''
        except:
            url = ''

get_url()
print(url)

available_quality_names = ['Нет ремонта','Косметический','Евро','Дизайнерский']
dict_qual = {'Нет ремонта':'no','Косметический':'cosmetic','Евро':'euro','Дизайнерский':'desing'}