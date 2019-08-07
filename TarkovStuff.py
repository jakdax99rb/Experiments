'''
Not really sure what I'm going to do with this but I want to make something to help me in tarkov.
If I can maybe crawl through the tarkov wiki to get up to date information on all weapon parts I could have something that will show me best in slot parts for each stat, weight, ergo, recoil, etc.
Yea Ill try a crawler.
'''
import re
import bs4
import requests
import json


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

    mainSite = 'https://escapefromtarkov.gamepedia.com'
    modsPage = 'https://escapefromtarkov.gamepedia.com/Weapon_mods'

    res = requests.get(modsPage)
    res.raise_for_status
    scraper = bs4.BeautifulSoup(res.text, 'html.parser')


def itemScraper(itemLink):

    # right hand panel template for label '<td class="va-infobox-label" title="" colspan="1" style="">.?</td>'
    # The target is whatever is in the .? section.
    # wrap loop in a try catch just incase a catagory isnt there like accuracy.

    itemName = r'#va-infobox0 > tbody > tr.va-infobox-row-title > td > div'
    typeSelector = r'#va-infobox0-content > td > table:nth-child(3) > tbody > tr:nth-child(4) > td.va-infobox-content'
    weightSelector = r'#va-infobox0-content > td > table:nth-child(3) > tbody > tr:nth-child(6) > td.va-infobox-content'

    recoilSelector = r'#va-infobox0-content > td > table:nth-child(5) > tbody > tr:nth-child(4) > td.va-infobox-content > font'
    ergonimicsSelector = r'#va-infobox0-content > td > table:nth-child(5) > tbody > tr:nth-child(6) > td.va-infobox-content > font'
    accuracySelector = r'#va-infobox0-content > td > table:nth-child(5) > tbody > tr:nth-child(8) > td.va-infobox-content > font'

    item = Item()

    item.dict(link) = itemLink

# tabber-3ff1495eea2bae6d04667e261b9f12de > div:nth-child(2) > p > a
# tabber-bbdbea9d2789de83c11cfc53c642181e > div:nth-child(2) > p > a
#tabber-fe0ce6fd1b8cb8898b54974ed4a776fc > div > p > a
