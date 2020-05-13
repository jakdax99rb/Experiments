import json
import mysql.connector
import random
import re

# writes sql code for the creation of an sql database


def sqlInserter(bigArray):

    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='school_project')
    cursor = cnx.cursor()

    for item in bigArray['itemArray']:

        sqlString = ('insert into item (url, value) Values (\'' +
                     item['itemLink'] + '\', ' + str(random.randint(1000, 1000000)) + ')')
        print(sqlString)
        cursor.execute(sqlString)
        cnx.commit()

    for item in bigArray['suppressorArray']:

        sqlString = ('Insert into suppressor '
                     '(item_url, recoil_mod, ergo_mod) '
                     'Values (( select url from item where url = \'' +
                     item['itemLink'] + '\'), ' + str(item['recoil%'])
                     + ', ' + str(item['ergonomics']) + ')')
        print(sqlString)
        cursor.execute(sqlString)

    cnx.commit()

    for item in bigArray['weaponArray']:

        sqlString = ('Insert into firearm '
                     '(item_url, recoil, ergonomics, type) '
                     'Values (( select url from item where url = \'' +
                     item['itemLink'] + '\'), ' +
                     str(item['horizontalRecoil'] + item['verticalRecoil'])
                     + ', ' + str(item['ergonomics']) + ', \'' + item['type'] + '\'' + ')')
        print(sqlString)
        cursor.execute(sqlString)

    cnx.commit()

    for item in bigArray['ammoArray']:

        sqlString = ('Insert into caliber '
                     '(item_url, damage, penetration) '
                     'Values (( select url from item where url = \'' +
                     item['itemLink'] + '\'), ' + str(item['damage'])
                     + ', ' + str(item['penetrationpower']) + ')')
        print(sqlString)
        cursor.execute(sqlString)

    cnx.commit()

    for item in bigArray['armorArray']:

        sqlString = ('Insert into armor'
                     '(item_url, zone, class) '
                     'Values (( select url from item where url = \'' +
                     item['itemLink'] + '\'), ' +
                     '\'' + item['armorzones'] + '\''
                     + ', ' + str(item['armorclass']) + ')')
        print(sqlString)
        cursor.execute(sqlString)

    cnx.commit()

    for item in bigArray['attachmentArray']:

        sqlString = ('Insert into attachment '
                     '(item_url, recoil_mod, ergo_mod) '
                     'Values (( select url from item where url = \'' +
                     item['itemLink'][:100] + '\'), ' + str(item['recoil%'])
                     + ', ' + str(item['ergonomics']) + ')')
        print(sqlString)
        cursor.execute(sqlString)

    # handle the closing of everything.
    cnx.commit()
    cursor.close()
    cnx.close()


def compatInserter(bigArray):

    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='school_project')
    cursor = cnx.cursor()

    for item in bigArray['attachmentArray']:

        for compat in item['Compatibility']:

            temp = 'https://escapefromtarkov.gamepedia.com' + compat

            for compat2 in bigArray['itemArray']:

                if 'type' in compat2:

                    if 'Compatibility' in compat2 and compat2['type'] != 'Suppressor' and 'recoil%' in compat2 and 'ergonomics' in compat2 and compat2['itemLink'] == temp:
                        '''
                        sqlString = ('Insert into attachement_compat '
                                     '(attachment_url, compatible_attachment) '
                                     'Values (( select url from item where url = \'' +
                                     item['itemLink'][:100] +
                                     '\'), (select url from item where url = \''
                                     + compat2['itemLink'][:100] + '\'))')
                        print(sqlString)
                        cursor.execute(sqlString)
                        '''
                    elif 'horizontalRecoil' in compat2 and compat2['itemLink'] == temp:

                        sqlString = ('Insert into firearm_compat '
                                     '(attachment_url, compatible_firearm) '
                                     'Values (( select url from item where url = \'' +
                                     item['itemLink'][:100] +
                                     '\'), (select url from item where url = \''
                                     + compat2['itemLink'][:100] + '\'))')
                        print(sqlString)
                        cursor.execute(sqlString)

    # handle the closing of everything.
    cnx.commit()
    cursor.close()
    cnx.close()


def armorPen(bigArray):

    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='school_project')
    cursor = cnx.cursor()

    for ammo in bigArray['ammoArray']:

        for x in range(2, 6):

            if int(ammo['penetrationpower']) / 10 >= x:

                sqlString = ('Insert into penetrates '
                             '(caliber_url, armor_class) '
                             'Values (( select url from item where url = \'' +
                             ammo['itemLink'][:100] +
                             '\'), ( ' + str(x) + '))')
                print(sqlString)
                cursor.execute(sqlString)

    # handle the closing of everything.
    cnx.commit()
    cursor.close()
    cnx.close()


def traderInserter(bigArray):

    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='school_project')
    cursor = cnx.cursor()

    cursor.execute('insert into traders (trader_name) Values (\'Jaeger LL1\')')
    cursor.execute(
        'insert into traders (trader_name) Values (\'Therapist LL1\')')
    cursor.execute('insert into traders (trader_name) Values (\'Prapor LL1\')')
    cursor.execute(
        'insert into traders (trader_name) Values (\'Peacekeeper LL1\')')
    cursor.execute('insert into traders (trader_name) Values (\'Skier LL1\')')
    cursor.execute(
        'insert into traders (trader_name) Values (\'Mechanic LL1\')')
    cursor.execute('insert into traders (trader_name) Values (\'Ragman LL1\')')

    cursor.execute('insert into traders (trader_name) Values (\'Jaeger LL2\')')
    cursor.execute(
        'insert into traders (trader_name) Values (\'Therapist LL2\')')
    cursor.execute('insert into traders (trader_name) Values (\'Prapor LL2\')')
    cursor.execute(
        'insert into traders (trader_name) Values (\'Peacekeeper LL2\')')
    cursor.execute('insert into traders (trader_name) Values (\'Skier LL2\')')
    cursor.execute(
        'insert into traders (trader_name) Values (\'Mechanic LL2\')')
    cursor.execute('insert into traders (trader_name) Values (\'Ragman LL2\')')

    cursor.execute('insert into traders (trader_name) Values (\'Jaeger LL3\')')
    cursor.execute(
        'insert into traders (trader_name) Values (\'Therapist LL3\')')
    cursor.execute('insert into traders (trader_name) Values (\'Prapor LL3\')')
    cursor.execute(
        'insert into traders (trader_name) Values (\'Peacekeeper LL3\')')
    cursor.execute('insert into traders (trader_name) Values (\'Skier LL3\')')
    cursor.execute(
        'insert into traders (trader_name) Values (\'Mechanic LL3\')')
    cursor.execute('insert into traders (trader_name) Values (\'Ragman LL3\')')

    cursor.execute('insert into traders (trader_name) Values (\'Jaeger LL4\')')
    cursor.execute(
        'insert into traders (trader_name) Values (\'Therapist LL4\')')
    cursor.execute('insert into traders (trader_name) Values (\'Prapor LL4\')')
    cursor.execute(
        'insert into traders (trader_name) Values (\'Peacekeeper LL4\')')
    cursor.execute('insert into traders (trader_name) Values (\'Skier LL4\')')
    cursor.execute(
        'insert into traders (trader_name) Values (\'Mechanic LL4\')')
    cursor.execute('insert into traders (trader_name) Values (\'Ragman LL4\')')

    for item in bigArray['itemArray']:

        if 'soldby' in item:

            sqlString = ('Insert into trader_buys '
                         '(trader_name, item_url, amount) '
                         'Values (( select trader_name from traders where trader_name = \'' +
                         re.search('^[a-zA-Z]+ LL\d', item['soldby'])[0] +
                         '\'), ( select url from item where url = \'' + item['itemLink'][:100] + '\'), ' + str(random.randint(1, 1000)) + ' )')
            print(sqlString)
            cursor.execute(sqlString)
            cnx.commit()

            sqlString = ('Insert into trader_sells '
                         '(trader_name, item_url, amount) '
                         'Values (( select trader_name from traders where trader_name = \'' +
                         re.search('^[a-zA-Z]+ LL\d', item['soldby'])[0] +
                         '\'), ( select url from item where url = \'' + item['itemLink'][:100] + '\'), ' + str(random.randint(1, 1000)) + ' )')
            print(sqlString)
            cursor.execute(sqlString)
            cnx.commit()

    # handle the closing of everything.
    cnx.commit()
    cursor.close()
    cnx.close()


def fireArmCompatFixer():

    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='school_project')
    cursor = cnx.cursor()

    sqlString = ('create table firearm_compat'
                 '(attachment_url varchar(100) not null references attachment (item_url),'
                 'compatible_firearm varchar(100) not null references firearm (item_url),'
                 'Primary key (attachment_url, compatible_firearm))')

    print(sqlString)
    cursor.execute(sqlString)

    # handle the closing of everything.
    cnx.commit()
    cursor.close()
    cnx.close()


def chamberInserter(bigArray):

    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='school_project')
    cursor = cnx.cursor()

    cursor.execute('drop table chambers')
    cursor.execute('Create table chambers(caliber_url varchar(100) not null references caliber(item_url) on delete cascade on update cascade'
                   ', firearm_url varchar(100) not null references firearm (item_url) on delete cascade on update cascade,'
                   ' Primary key (caliber_url, firearm_url))')

    for item in bigArray['weaponArray']:

        for ammo in bigArray['ammoArray']:

            if ammo['itemName'] == item['defaultammo']:

                sqlString = ('Insert into chambers '
                             '(caliber_url, firearm_url) '
                             'Values (( select item_url from caliber where item_url = \'' +
                             ammo['itemLink'][:100] +
                             '\'), ( select url from item where url = \'' + item['itemLink'][:100] + '\'))')
                print(sqlString)
                cursor.execute(sqlString)

    # handle the closing of everything.
    cnx.commit()
    cursor.close()
    cnx.close()


def sortItemsIntoArrays(itemArray):
    # Sort every item into the various sub classes by using multiple different arrays to make future stuff easier.

    suppressorArray = []
    weaponArray = []
    ammoArray = []
    armorArray = []
    attachmentArray = []
    tempArray = []

    for v in itemArray:
        if v not in tempArray:
            tempArray.append(v)

    itemArray = tempArray

    for item in itemArray:

        if 'horizontalRecoil' in item:

            weaponArray.append(item)

        if 'type' in item:

            if item['type'] == 'Suppressor':

                suppressorArray.append(item)

            if 'Compatibility' in item and item['type'] != 'Suppressor' and 'recoil%' in item and 'ergonomics' in item:

                attachmentArray.append(item)

        if 'penetrationpower' in item:

            ammoArray.append(item)

        if 'armorclass' in item:

            armorArray.append(item)

    bigArray = {'suppressorArray': suppressorArray, 'weaponArray': weaponArray,
                'ammoArray': ammoArray, 'armorArray': armorArray, 'attachmentArray': attachmentArray, 'itemArray': itemArray}

    return bigArray


def miscInserter(bigArray):

    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='school_project')
    cursor = cnx.cursor()

    # creates players
    for x in range(41):

        sqlString = ('Insert into player '
                     '(username, level, money) '
                     'Values ((\'player' +
                     str(x) +
                     '\'), (' + str(random.randint(1, 40)) + '), (' + str(random.randint(1, 1000000)) + '))')
        print(sqlString)
        cursor.execute(sqlString)

    # creates a bunch of owned items
    for y in range(160):

        itemToOwn = bigArray['itemArray'][y]

        sqlString = ('Insert into owns '
                     '(player_name, amount, item_url) '
                     'Values ((select username from player where username = \'player' +
                     str(int(y/4)) +
                     '\'), (' + str(random.randint(1, 50)) + '), ( select url from item where url = \'' + str(itemToOwn['itemLink']) + '\'))')
        print(sqlString)
        cursor.execute(sqlString)

    # create data for player buys
    for y in range(160):

        itemToOwn = bigArray['itemArray'][y+160]

        sqlString = ('Insert into player_buys '
                     '(username, amount, item_url) '
                     'Values ((select username from player where username = \'player' +
                     str(int(y/4)) +
                     '\'), (' + str(random.randint(1, 50)) + '), ( select url from item where url = \'' + str(itemToOwn['itemLink'][:100]) + '\'))')
        print(sqlString)
        cursor.execute(sqlString)

    # create data for player sales
    for y in range(160):

        itemToOwn = bigArray['itemArray'][y+320]

        sqlString = ('Insert into player_sells '
                     '(username, amount, item_url) '
                     'Values ((select username from player where username = \'player' +
                     str(int(y/4)) +
                     '\'), (' + str(random.randint(1, 50)) + '), ( select url from item where url = \'' + str(itemToOwn['itemLink'][:100]) + '\'))')
        print(sqlString)
        cursor.execute(sqlString)

    # create data for player trades
    for y in range(120):

        itemToOwn = bigArray['itemArray'][y+160]

        sqlString = ('Insert into trade '
                     '(buyer, seller, cost, item_url) '
                     'Values ((select username from player where username = \'player' +
                     str(int(y/4+1)) +
                     '\'),' + '(select username from player where username = \'player' +
                     str(int(y/4)) +
                     '\'),' + '(' + str(random.randint(1, 1000000)) + '), ( select url from item where url = \'' + str(itemToOwn['itemLink']) + '\'))')
        print(sqlString)
        cursor.execute(sqlString)

    for y in range(10):

        sqlString = ('Insert into suppressed '
                     '(suppressor_url, firearm_uid) '
                     'Values ((select item_url from suppressor where item_url = \'' +
                     bigArray['suppressorArray'][y]['itemLink'] +
                     '\'),' + '(select uid from firearm where uid = ' +
                     str(int(y+1)) + '))')
        print(sqlString)
        cursor.execute(sqlString)

    for y in range(10, 20):

        sqlString = ('Insert into fitted_to '
                     '(attachment_url, firearm_uid) '
                     'Values ((select item_url from attachment where item_url = \'' +
                     bigArray['attachmentArray'][y]['itemLink'] +
                     '\'),' + '(select uid from firearm where uid = ' +
                     str(int(y+1)) + '))')
        print(sqlString)
        cursor.execute(sqlString)

    cnx.commit()
    cursor.close()
    cnx.close()


with open('itemJSON.json', 'r') as file:

    itemArray = json.loads(file.read())


# run the various functions here, make sure you do them in proper order so you dont get foreign key failures
# also make sure that you run the sortItemsIntoArrays as the argument to whatever function you are running.
fireArmCompatFixer()
compatInserter(sortItemsIntoArrays(itemArray))
