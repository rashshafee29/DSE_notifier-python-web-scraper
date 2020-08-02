import json
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'home/index.html')


def scrap(request):
    res = requests.get('https://www.dsebd.org/')

    # print(res.text)

    soup = BeautifulSoup(res.text, 'lxml')
    # print(soup.prettify())
    list1 = []

    k = soup.find_all('div', {'class': 'Scroller'})
    for quote in k:
        tds = (quote.findAll('td'))
        for val in tds:
            val2 = val.findAll('tr')
            for val3 in val2:
                val4 = val3.findAll('a')
                for val5 in val4:
                    # print(val5)
                    list1.append(val5.text)
        # print(quote.text)
    name = []
    current = []
    changeValue = []
    percentageValue = []
    json_list = (json.dumps(list1))
    for item in list1:
        m_s = ' '.join(item.split())
        name.append(m_s.split(" ")[0])
        current.append(m_s.split(" ")[1])
        changeValue.append(float(m_s.split(" ")[2]))
        percentageValue.append(m_s.split(" ")[3])

    allList  = zip(name, current, changeValue, percentageValue)


    # Getting time and market close or open information
    isStart = 0
    isClosed = False
    time = soup.find_all('span', {'class': 'time'})
    # print(time)
    time_list = []
    for time_i in time:
        # print(time_i.text)
        time_list.append(time_i.text)
    timeNow = time_list[0]
    if time_list[2] == 'Market Status: Closed':
        isClosed = True
        if time_list[1].split(" ")[3] == 'PM':
            isStart = 1
        else:
            isStart = 0

    if isClosed:
        print(timeNow)
        print(isStart)
    return render(request, 'home/index.html', {"allList": allList})

