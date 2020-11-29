import requests
import re
import os
import time

header = {
    r'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Referer': 'https://www.google.com'}
places_dicts = {}
available = [[0 for times in range(10)] for places in range(7)]


def initDicts():
    url = r"http://hqcggl.ouc.edu.cn/website/findPlaceList"
    myData = {'typeId': '3bf3df97-53a8-46bf-b334-90a0bc6235d9'}
    r = requests.post(url, data=myData)
    datas = r.text.split('allList":[{"')[1].split('"}],"list')[0].split('"},{"')
    for data in datas:
        temp = data.replace(',', ':').split('":"')
        places_dicts[temp[1].strip()] = temp[3].strip();



def main():
    initDicts()
    print(places_dicts)


main()
