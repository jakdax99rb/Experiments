import re
import bs4
import requests
import lxml
import csv
import json


def wikiScraper():

    itemList = []
    linkList = []
    res = requests.get(
        'https://docs.google.com/spreadsheets/d/1C4TVq6cIoJhXD_9Re2_FtWxHykZTRF1msvXsPV_-utc/export?format=tsv')

    for line in res.text.splitlines():

        line_split = line.split("\t")

        if(len(line_split) > 1 and line_split[1] != "" and 'Weapons#' not in line_split[1]):

            linkList.append(line_split[1])

    for x in range(0, len(linkList)):

        itemList.append(itemScraper(linkList[x]))

    masterKeyList = []

    for key in itemList[0].keys():

        masterKeyList.append(str(key))

    with open('itemJSON.json', 'w') as file:

        file.write(json.dumps(itemList, sort_keys=True,
                              indent=4).replace('\xa0', ''))


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
    item = {}

    item['itemLink'] = itemLink
    item['itemName'] = scraper.find(
        'h1', attrs={'class': 'firstHeading'}).get_text()

    for z in range(0, len(labelList)):

        labelList[z] = labelList[z].get_text().lower().replace(
            '\u00a0', '').replace(' ', '')

        if 'vertical' in contentList[z].get_text().lower().strip():

            recoilNumbers = re.findall(r'\d+', contentList[z].get_text())
            item['verticalRecoil'] = float(recoilNumbers[0])
            item['horizontalRecoil'] = float(recoilNumbers[1])

        elif labelList[z] == 'weight':

            item[labelList[z]] = float(
                contentList[z].get_text().lower().replace(' ', '').replace('kg', ''))

        elif labelList[z] == 'ergonomics':

            item[labelList[z]] = float(
                contentList[z].get_text().replace('+', '').replace(' ', ''))

        elif labelList[z] == 'examineexperience' and not contentList[z].get_text() == 'Examined by default':

            item[labelList[z]] = float(
                contentList[z].get_text().replace('+', '').replace(' ', ''))
                
        elif labelList[z] == 'lootexperience':

            item[labelList[z]] = float(
                contentList[z].get_text().replace('+', '').replace(' ', ''))
        
        elif labelList[z] == 'accuracy':

            item[labelList[z]] = float(
                re.findall(r'\d',contentList[z].get_text().replace('+', '').replace(' ', '')[1])

        elif labelList[z] == 'muzzlevelocity':

            item[labelList[z]] = float(
                contentList[z].get_text().replace('+', '').replace(' ', ''))


        elif labelList[z] == 'recoil%' and not 'vertical' in contentList[z].get_text().lower().strip():

            item[labelList[z]] = float(
                contentList[z].get_text().replace('+', '').replace(' ', ''))

        else:

            item[labelList[z]] = contentList[z].get_text().replace('+', '')

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

        stat = 'recoil%'

    elif stat.lower().strip() == ('ergo' or 'ergonomics'):

        stat = 'ergonomics'

    itemType = itemType.replace(' ', '').lower()
    itemType = itemType.replace('/', '')

    with open(itemType + '.json', 'r') as file:

        myArray = json.loads(file.read())

    bestItem = myArray[0]

    for item in myArray:

        try:

            if stat == 'ergonomics':

                if item[stat] > bestItem[stat]:

                    bestItem = item

                elif item[stat] == bestItem[stat] and item['Recoil%'] < bestItem['Recoil%']:

                    bestItem = item

            elif item[stat] <= bestItem[stat]:

                bestItem = item

            elif item[stat] == bestItem[stat] and item['Ergonomics'] > bestItem['Ergonomics']:

                bestItem = item

        except:

            print('Error in stat comparision process.\nStat given is: ' +
                  stat + '\nItem given is: ' + item['itemLink'])

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


wikiScraper()
# sortJSONByitemType()
# print(getBestStat('suppressor', 'recoil')['itemName'])
'''
with open('itemJSON.json', 'r') as file:

    myDict = json.loads(file.read())

print(myDict[0]['itemName'])
'''
