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
    regSelect = '>.*<'
    typeSelect = '/">.*<//a'

    selectorDict = {
        'itemName': r'#va-infobox0 > tbody > tr.va-infobox-row-title > td > div',
        'type': r'#va-infobox0-content > td > table:nth-child(3) > tbody > tr:nth-child(4) > td.va-infobox-content',
        'weight': r'#va-infobox0-content > td > table:nth-child(3) > tbody > tr:nth-child(6) > td.va-infobox-content',
        'recoil': r'#va-infobox0-content > td > table:nth-child(5) > tbody > tr:nth-child(4) > td.va-infobox-content > font',
        'ergonimics': r'#va-infobox0-content > td > table:nth-child(5) > tbody > tr:nth-child(6) > td.va-infobox-content > font',
        'accuracy': r'#va-infobox0-content > td > table:nth-child(5) > tbody > tr:nth-child(8) > td.va-infobox-content > font',
        'muzzleVelocity': r'#va-infobox0-content > td > table:nth-child(7) > tbody > tr:nth-child(4) > td.va-infobox-content > font',
        # 'seller': r'#va-infobox0-content > td > table:nth-child(3) > tbody > tr:nth-child(10) > td.va-infobox-content > a',
        'capacity': r'#va-infobox0-content > td > table:nth-child(5) > tbody > tr:nth-child(14) > td.va-infobox-content',
        'caliber': r'#va-infobox0-content > td > table:nth-child(7) > tbody > tr:nth-child(4) > td.va-infobox-content > a',
        'compatibility': r'#mw-content-text > div > div'
    }

    item.dict['itemLink'] = itemLink

    for k, v in selectorDict.items():
        if(k == 'type'):

            target = re.search(typeSelect, str(scraper.select(v)))

            if(target):

                target = re.sub('/">', '', target.group(0))
                target = re.sub('<//a', '', target)
                target = target.strip()
                item.dict[k] = str(target)

        elif(k == 'weight'):

            target = re.search(regSelect, str(scraper.select(v)))

            if(target):

                target = re.sub('>', '', target.group(0))
                target = re.sub('<', '', target)
                target = re.sub('kg', '', target, flags=re.I)
                target = target.strip()
                try:
                    item.dict[k] = float(target)
                except:
                    print(itemLink)
                    print(target)

        elif(k == 'itemName'):

            target = re.search(regSelect, str(scraper.select(v)))

            if(target):
                target = re.sub('>', '', target.group(0))
                target = re.sub('<', '', target)
                target = target.strip()
                item.dict[k] = str(target)

        elif(k == 'seller'):

            target = re.search(regSelect, str(scraper.select(v)))

            if(target):
                target = re.sub('>', '', target.group(0))
                target = re.sub('<', '', target)
                target = target.strip()
                item.dict[k] = str(target)

        elif(k == 'caliber'):

            target = re.search(regSelect, str(scraper.select(v)))

            if(target):
                target = re.sub('>', '', target.group(0))
                target = re.sub('<', '', target)
                target = target.strip()
                item.dict[k] = str(target)

        elif(k == 'compatibility'):

            compatdiv = scraper.find("div", attrs={"title": "Compatibility"})

            if compatdiv:

                compatList = []

                for a in compatdiv.find_all("a"):

                    compatList.append(a.get_text())

                item.dict[k] = compatList

        # Base Case
        else:

            compatdiv = scraper.find("div", attrs={"title": "Compatibility"})

            if compatdiv:

                compatList = []

                for a in compatdiv.find_all("a"):

                    compatList.append(a.get_text())

                item.dict[k] = compatList

    # Loyalty level handling below
    '''
    target = re.search(r'LL\d?', str(res.text))

    if(target):

        target = str(target.group(0))
        target = target.strip()
        item.dict['loyaltyLevel'] = str(target)
    '''

    return item


wikiScraper()
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
