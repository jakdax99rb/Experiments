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


class Item():

    def __init__(self):

        self.dict = {

            # This dict wil be dynamically created based on the content of each page.
            # Compatibilities will be stored as an array of strings.
            # Delete every column after you get what you need.
            # Use a while loop with that checks to see if there are any entries left to pull.
            # Use the table to go through and get links to the object and not stats. Write scaper for individual pages first.
        }


def wikiScraper():

    itemList = []
    linkList = []
    res = requests.get(
        'https://docs.google.com/spreadsheets/d/1C4TVq6cIoJhXD_9Re2_FtWxHykZTRF1msvXsPV_-utc/export?format=tsv')

    for line in res.text.splitlines():

        line_split = line.split("\t")

        if(len(line_split) > 1 and line_split[1] != ""):

            linkList.append(line_split[1])

    for link in linkList:

        itemList.append(itemScraper(link))

    print(itemList[30].dict['itemName'])

    '''
    uri = 'https://docs.google.com/spreadsheets/d/1m8oFMO9OKdEg2nZdTytMTEl_oZfLl9AJIYdE5dalHUA/gviz/tq?tqx=out:csv'

    with requests.Session() as session:
        download session.get(uri)

        content = download.content.decode('utf-8')

        splitContent = csv.reader(decoded_content.splitlines(), delimiter=',')
        tarkovDict = list(splitContent)
        for row in tarkovDict
        with open('tarkov.csv', mode='w') as csv_file:
            fieldnames = ['endpoint', 'url']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({tarkovDict})
        '''


def itemScraper(itemLink):

    res = requests.get(itemLink)
    res.raise_for_status
    scraper = bs4.BeautifulSoup(res.text, 'html.parser')
    item = Item()
    labelList = scraper.find_all("td", attrs={"class": "va-infobox-label"})
    contentList = scraper.find_all("td", attrs={"class": "va-infobox-content"})
    labelArray = []
    contentArray = []
    item = Item()

    for x in labelList:

        labelArray.append(x.get_text())

    for y in contentList:

        contentArray.append(y.get_text())

    for z in range(0, len(labelArray)):

        item.dict[labelArray[z]] = contentArray[z]

    compatdiv = scraper.find("div", attrs={"title": "Compatibility"})

    if compatdiv:

        compatList = []

        for a in compatdiv.find_all("a"):

            compatList.append(a.get_text())

        item.dict['Compatibility'] = compatList

    return item


# wikiScraper()
'''
print('')
print('')
item = itemScraper(
    'https://escapefromtarkov.gamepedia.com/Direct_Thread_Mount_adapter_for_Silencerco_Hybrid_46.')
for k, v in item.dict.items():
    print(k, v)
print('')
print('')
'''


for k, v in itemScraper('https://escapefromtarkov.gamepedia.com/Magpul_AFG_grip').dict.items():
    print(k, v)
