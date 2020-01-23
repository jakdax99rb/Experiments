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

        # stop gap to handle some errant links being passed from the google doc.
        if(linkList[x] != ('https://escapefromtarkov.gamepedia.com' and '.')):

            itemList.append(itemScraper(linkList[x]))

    masterKeyList = []

    for key in itemList[0].keys():

        masterKeyList.append(str(key))

    with open('itemJSON.json', 'w') as file:

        file.write(json.dumps(itemList, sort_keys=True,
                              indent=4).replace('\xa0', ''))


def itemScraper(itemLink):

    # This function actually gets the info from every link passed to it.
    # Once its scraped everything dynamically it returns a dict called item that contains all the stuff

    print(itemLink)

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

            contentList[z] = contentList[z].get_text().replace(
                '+', '').replace(' ', '').replace('m/s', '')

            if len(re.findall(r'\d+', contentList[z])) > 1:

                item[labelList[z]] = float(
                    re.findall(r'\d+', contentList[z])[1])

            else:

                item[labelList[z]] = float(contentList[z])

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


# takes in a string itemType to select the type of item to pull from
# also takes in a stat string to select the proper section in the if sections
# I was going to use a switch case but didnt have enough time to get a hold on how to execute code in a switch case in python.


def getBestInStat(itemType,  stat):

    stat = stat.strip().lower()

    if stat == 'recoil':

        return recoil(itemType)

    elif stat == 'ergonomics':

        return ergonomics(itemType)

    elif stat == 'weight':

        return weight(itemType)

    elif stat == 'muzzlevelocity':

        return muzzleVelocity(itemType)

    elif stat == 'combinedrecoil':

        return combinedRecoil(itemType)


def recoil(itemType):
    # this array will store the best items initially in backwards order (array.length-1 will store best)
    # Ill reverse this for display later
    sortedBestArray = []

    with open('itemJSON.json', 'r') as file:

        myArray = json.loads(file.read())

    sortedBestArray.append(myArray[0])

    for item in myArray:

        try:

            if item['type'].lower() == itemType.lower():

                if item['recoil%'] < sortedBestArray[len(sortedBestArray)-1]['recoil%']:

                    sortedBestArray.append(item)

                elif item['recoil%'] == sortedBestArray[len(sortedBestArray)-1]['recoil%']:

                    if item['ergonomics'] > sortedBestArray[len(sortedBestArray)-1]['recoil%']:

                        sortedBestArray.append(item)

        except:
            print("Stat not found \n" + "itemType: " +
                  itemType + 'stat: recoil%' + '\nitem link: ' + item["itemLink"])

    return sortedBestArray


def ergonomics(itemType):

    ergonomicsBest = 0
    sortedBestArray = []

    with open('itemJSON.json', 'r') as file:

        myArray = json.loads(file.read())

    for item in myArray:

        try:

            if item['type'].lower() == itemType.lower():

                if item['ergonomics'] > ergonomicsBest:

                    sortedBestArray.append(item)
                    ergonomicsBest = item['ergonomics']

                elif item['ergonomics'] == ergonomicsBest:

                    if item['recoil%'] < sortedBestArray[len(sortedBestArray)-1]['recoil%']:

                        sortedBestArray.append(item)

        except:
            print("Stat not found \n" + "itemType: " +
                  itemType + 'stat: ergonomics' + '\nitem link: ' + item["itemLink"])

    return sortedBestArray


def weight(itemType):

    weightBest = 100000000
    sortedBestArray = []

    with open('itemJSON.json', 'r') as file:

        myArray = json.loads(file.read())

    for item in myArray:

        try:

            if item['type'].lower() == itemType.lower():

                if item['weight'] < weightBest:

                    weightBest = item['weight']

                elif item['weight'] == weightBest:

                    if item['ergonomics'] > sortedBestArray[len(sortedBestArray)-1]["ergonomics"]:

                        sortedBestArray.append(item)

        except:
            print("Stat not found \n" + "itemType: " +
                  itemType + 'stat: weight' + '\nitem link: ' + item["itemLink"])

    return sortedBestArray


def muzzleVelocity(itemType):

    muzzleVelocityBest = 0
    sortedBestArray = []

    with open('itemJSON.json', 'r') as file:

        myArray = json.loads(file.read())

    for item in myArray:

        try:

            if item['type'].lower() == itemType.lower():

                if item['muzzlevelocity'] > muzzleVelocityBest:

                    sortedBestArray.append(item)
                    muzzleVelocityBest = item['muzzlevelocity']

                elif item['muzzlevelocity'] == muzzleVelocityBest:

                    if item['ergonomics'] < sortedBestArray[len(sortedBestArray)-1]['ergonomics']:

                        sortedBestArray.append(item)

        except:
            print("Stat not found \n" + "itemType: " +
                  itemType + 'stat: muzzleVelocity' + '\nitem link: ' + item["itemLink"])

    return sortedBestArray


def combinedRecoil(itemType):

    sortedBestArray = []
    combinedRecoilBest = 100000000000
    combinedRecoilTemp = 0

    with open('itemJSON.json', 'r') as file:

        myArray = json.loads(file.read())

    for item in myArray:

        try:

            if item["type"].lower() == itemType.lower():

                combinedRecoilTemp = (
                    item['horizontalRecoil'] + item['verticalRecoil'])

                if combinedRecoilTemp < combinedRecoilBest:

                    combinedRecoilBest = combinedRecoilTemp
                    sortedBestArray.append(item)

                elif combinedRecoilTemp == combinedRecoilBest:

                    if item['ergonomics'] > sortedBestArray[len(sortedBestArray)-1]['ergonomics']:

                        sortedBestArray.append(item)

        except:
            print("Stat not found \n" + "itemType: " +
                  itemType + 'stat: combinedRecoil' + '\nitem link: ' + item["itemLink"])
    return sortedBestArray


'''

def sortJSONByitemType():
    # This code is no longer needed.
    # This function sorts all of the items in itemJSON.json into a bunch of individual json files to make it easier when looking for the best items in each catagory.
    # this array stores a string value for every array already created.
    arraysAlreadyMade = []
    bigArray = []

    with open('itemJSON.json', 'r') as file:

        myDict = json.loads(file.read())

    for item in myDict:

        try:

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

        except:

            print(item['itemLink'] + ' :This thing doesnt have a type.\n')

    for array in bigArray:

        arrayType = array[0]['type']
        arrayType = arrayType.replace(' ', '').lower()
        arrayType = arrayType.replace('/', '')

        with open(arrayType+'.json', 'w') as file:

            file.write(json.dumps(array, sort_keys=True, indent=4))

'''

'''

This is depreciated at this point, I originally wrote it to go through and get every catagory(recoil, ergo, muzzle velocity) etc. but turns out
it wasnt really needed.

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

'''
'''

Wrote a better way but Im keeping this just in case I ever need to look back at it.

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

'''



# sortJSONByitemType()
# wikiScraper()
best = getBestInStat('Assault rifle', 'ergonomics')
print(best[len(best)-1]['itemLink'])
# sortJSONByitemType()

'''
with open('itemJSON.json', 'r') as file:

    myDict = json.loads(file.read())

print(myDict[0]['itemName'])
'''
