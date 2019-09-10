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

        file.write(json.dumps(itemList).replace('\xa0', ''))

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
        'itemType': '',
        'Weight': '',
        'Grid size': '',
        'Recoil%': '',
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
        'Ergonomics%': '',
        'Check Speed Modifier%': '',
        'loads/Unloads Speed Modifier%': '',
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

        contentArray.append(y.get_text().replace('+', ''))

    for z in range(0, len(labelArray)):

        item[labelArray[z]] = contentArray[z]

    compatdiv = scraper.find("div", attrs={"title": "Compatibility"})

    if compatdiv:

        compatList = []

        for a in compatdiv.find_all("a"):

            compatList.append(a.get_text())

        item['Compatibility'] = compatList

    return item

# only ever give numeric stats.


def getBestStat(itemType, stat):

    if stat.lower().strip() == 'recoil':

        stat = 'Recoil%'

    elif stat.lower().strip() == ('ergo' or 'ergonomics'):

        stat = 'Ergonomics'

    itemType = itemType.replace(' ', '').lower()
    itemType = itemType.replace('/', '')

    with open(itemType + '.json', 'r') as file:

        myArray = json.loads(file.read())

    bestItem = myArray[0]

    for item in myArray:

        if stat == 'Ergonomics':

            if float(item[stat]) > float(bestItem[stat]):

                bestItem = item

            elif float(item[stat]) == float(bestItem[stat]) and float(item['Recoil%']) < float(bestItem['Recoil%']):

                bestItem = item

        elif float(item[stat]) <= float(bestItem[stat]):

            bestItem = item

        elif float(item[stat]) == float(bestItem[stat]) and float(item['Ergonomics']) > float(bestItem['Ergonomics']):

            bestItem = item

    return bestItem


def sortJSONByitemType():

    # this array stores a string value for every array already created.
    arraysAlreadyMade = []
    bigArray = []

    with open('itemJSON.json', 'r') as file:

        myDict = json.loads(file.read())

    for item in myDict:

        itemType = item['Type']
        itemType = itemType.replace(' ', '').lower()
        itemType = itemType.replace('/', '')

        if itemType == 'barrels':

            itemType = 'barrel'

        if itemType not in arraysAlreadyMade:

            arraysAlreadyMade.append(itemType)
            exec(itemType + '= []\n' + itemType +
                 '.append(item)\nbigArray.append(' + itemType + ')')

        else:

            exec(itemType + '.append(item)')

    for array in bigArray:

        arrayType = array[0]['Type']
        arrayType = arrayType.replace(' ', '').lower()
        arrayType = arrayType.replace('/', '')

        with open(arrayType+'.json', 'w') as file:

            file.write(json.dumps(array, sort_keys=True, indent=4))


# sortJSONByitemType()
print(getBestStat('suppressor', 'recoil')['itemName'])
'''
with open('itemJSON.json', 'r') as file:

    myDict = json.loads(file.read())

print(myDict[0]['itemName'])
'''
