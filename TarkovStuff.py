'''
Not really sure what I'm going to do with this but I want to make something to help me in tarkov.
If I can maybe crawl through the tarkov wiki to get up to date information on all weapon parts I could have something that will show me best in slot parts for each stat, weight, ergo, recoil, etc.
Yea Ill try a crawler.
'''
import re
import bs4
import requests
import lxml
import csv
import pygsheets
import threading
import operator
import json


def wikiScraper():

    itemList = []
    linkList = []
    res = requests.get(
        'https://docs.google.com/spreadsheets/d/1C4TVq6cIoJhXD_9Re2_FtWxHykZTRF1msvXsPV_-utc/export?format=tsv')

    for line in res.text.splitlines():

        line_split = line.split("\t")

        if(len(line_split) > 1 and line_split[1] != ""):

            linkList.append(line_split[1])

    for x in range(0, len(linkList)):

        itemList.append(itemScraper(linkList[x]))

    masterKeyList = []

    for key in itemList[0].keys():

        masterKeyList.append(str(key))

    with open('itemJSON.json', 'w') as file:

        file.write(json.dumps(itemList))

    return itemList


def keyGetter(itemList):

    masterKeyList = []
    tempKeyList = []

    for key in itemList[0].keys():

        masterKeyList.append(str(key))

    for x in range(1, len(itemList)):

        for key in itemList[x].keys():

            tempKeyList.append(str(key))

        for key in tempKeyList:

            if not (key in masterKeyList):

                masterKeyList.append(key)

    return masterKeyList


def itemScraper(itemLink):

    res = requests.get(itemLink)
    res.raise_for_status
    scraper = bs4.BeautifulSoup(res.text, 'html.parser')
    labelList = scraper.find_all("td", attrs={"class": "va-infobox-label"})
    contentList = scraper.find_all("td", attrs={"class": "va-infobox-content"})
    labelArray = []
    contentArray = []
    item = {
        'itemLink': '',
        'itemName': '',
        'Type': '',
        'Weight': '',
        'Grid size': '',
        'Recoil\xa0%': '',
        'Ergonomics': '',
        'Loot experience': '',
        'Examine experience': '',
        'Compatibility': '',
        'Sold by': '',
        'Modes': '',
        'Accuracy': '',
        'Muzzle velocity': '',
        'Sighting range': '',
        'Caliber': '',
        'Default ammo': '',
        'Accepted ammunition': '',
        'Ergonomics\xa0%': '',
        'Check Speed Modifier\xa0%': '',
        'Load/Unload Speed Modifier\xa0%': '',
        'Capacity': '',
        'Check Accuracy Level': '',
        'Slot': ''
    }

    item['itemLink'] = itemLink
    item['itemName'] = scraper.find(
        'h1', attrs={'class': 'firstHeading'}).get_text()

    for x in labelList:

        labelArray.append(x.get_text())

    for y in contentList:

        contentArray.append(y.get_text())

    for z in range(0, len(labelArray)):

        item[labelArray[z]] = contentArray[z]

    compatdiv = scraper.find("div", attrs={"title": "Compatibility"})

    if compatdiv:

        compatList = []

        for a in compatdiv.find_all("a"):

            compatList.append(a.get_text())

        item['Compatibility'] = compatList

    return item


'''
print('\n\n')
for k, v in itemScraper('https://escapefromtarkov.gamepedia.com/Magpul_AFG_grip').dict.items():
    print(k, v)
print('\n\n')
'''
wikiScraper()

'''
with open('itemJSON.json', 'r') as file:

    myDict = json.loads(file.read())

print(myDict[0]['itemName'])
'''
