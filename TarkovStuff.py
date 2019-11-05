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

        for x in range(0, len(line_split)):

            if x % 2 == 1:

                if(line_split[x] != "" and 'Weapons#' not in line_split[x]):

                    linkList.append(line_split[x])

    for x in range(0, len(linkList)):

        itemList.append(itemScraper(linkList[x]))

    masterKeyList = []

    for key in itemList[0].keys():

        masterKeyList.append(str(key))

    with open('itemJSON.json', 'w') as file:

        file.write(json.dumps(itemList, sort_keys=True,
                              indent=4).replace('\xa0', ''))


def keyGetter(itemList):
    '''
    This is depreciated at this point, I originally wrote it to go through and get every catagory(recoil, ergo, muzzle velocity) etc. but turns out
    it wasnt really needed.
    '''

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

    # This function actually gets the info from every link passed to it.
    # Once its scraped everything dynamically it returns a dict called item that contains all the stuff

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

        if 'vertical' in contentList[z].get_text().lower().strip() and not ('?' in contentList[z].get_text()):

            recoilNumbers = re.findall(r'\d+', contentList[z].get_text())
            item['verticalRecoil'] = float(recoilNumbers[0])
            item['horizontalRecoil'] = float(recoilNumbers[1])

        elif labelList[z] == 'weight' and not ('?' in contentList[z].get_text()):

            item[labelList[z]] = float(
                contentList[z].get_text().lower().replace(' ', '').replace('kg', '').replace(',', ''))

        elif labelList[z] == 'ergonomics' and not ('?' in contentList[z].get_text()):

            contentList[z] = contentList[z].get_text().replace(
                '+', '').replace(' ', '')

            if len(re.findall(r'\d+', contentList[z])) > 1:

                item[labelList[z]] = float(
                    re.findall(r'\d+', contentList[z])[1])

            else:

                item[labelList[z]] = float(contentList[z])

        elif labelList[z] == 'examineexperience' and not contentList[z].get_text() == 'Examined by default':

            item[labelList[z]] = float(
                contentList[z].get_text().replace('+', '').replace(' ', ''))

        elif labelList[z] == 'lootexperience' and not ('?' in contentList[z].get_text()):

            item[labelList[z]] = float(
                contentList[z].get_text().replace('+', '').replace(' ', ''))

        elif labelList[z] == 'accuracy' and not ('?' in contentList[z].get_text()):

            contentList[z] = contentList[z].get_text().replace(
                '+', '').replace(' ', '')

            if len(re.findall(r'\d+', contentList[z])) > 1:

                item[labelList[z]] = float(
                    re.findall(r'\d+', contentList[z])[1])

            else:

                item[labelList[z]] = float(contentList[z])

        elif labelList[z] == 'muzzlevelocity' and not ('?' in contentList[z].get_text()):

            item[labelList[z]] = float(
                contentList[z].get_text().replace('+', '').replace(' ', '').replace('m/s', ''))

        elif labelList[z] == 'recoil%' and not 'vertical' in contentList[z].get_text().lower().strip() and not ('?' in contentList[z].get_text()):

            item[labelList[z]] = float(
                contentList[z].get_text().replace('+', '').replace(' ', ''))

        elif not ('?' in contentList[z].get_text()):

            item[labelList[z]] = contentList[z].get_text().replace('+', '')

    compatdiv = scraper.find("div", attrs={"title": "Compatibility"})

    if compatdiv:

        compatList = []

        for a in compatdiv.find_all("a"):

            compatList.append(a.get('href'))

        item['Compatibility'] = compatList

    return item


def getBestStat(itemType, stat):

    # This gets the item with the best stat(recoil, ergo, etc.) right now it only fully functions for recoil and ergo as they are the most important stats.

    if stat.lower().strip() == 'recoil':

        stat = 'recoil%'

    elif stat.lower().strip() == ('ergo' or 'ergonomics'):

        stat = 'ergonomics'

    itemType = itemType.replace(' ', '').lower()
    itemType = itemType.replace('/', '')

    with open('itemJSON.json', 'r') as file:

        myArray = json.loads(file.read())

    bestItem = myArray[0]

    for item in myArray:

        if item['type'].lower() == itemType.lower():

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
    # This function sorts all of the items in itemJSON.json into a bunch of individual json files to make it easier when looking for the best items in each catagory.
    # I'll probably rewrite the logic behind choosing the best items in a catagory later so stuff doesnt need to be sorted into individual json files.
    # this array stores a string value for every array already created.
    arraysAlreadyMade = []
    bigArray = []

    with open('itemJSON.json', 'r') as file:

        myDict = json.loads(file.read())

    for item in myDict:

        itemType = item['type']
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

        arrayType = array[0]['type']
        arrayType = arrayType.replace(' ', '').lower()
        arrayType = arrayType.replace('/', '')

        with open(arrayType+'.json', 'w') as file:

            file.write(json.dumps(array, sort_keys=True, indent=4))


# sortJSONByitemType()
print(getBestStat('Handguard', 'recoil')['itemLink'])
'''
with open('itemJSON.json', 'r') as file:

    myDict = json.loads(file.read())

print(myDict[0]['itemName'])
'''
