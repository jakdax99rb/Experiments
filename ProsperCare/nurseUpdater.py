import os
import openpyxl
import re
import xlwings as xw
from win32com.client import Dispatch

sheetsToBeCopied = ['Data', 'MedicationFull', 'DxListFull', 'VitalsHistory',
                    'ClientPhysicians', 'VisitDates', 'SnHistorical', 'RNVisitFormHistorical']


def updater(fileName, newVersionName, officeType):

    if officeType == 'augusta':

        newWorkBookPath = (newVersionName + ' Augusta.xlsm')
    else:
        newWorkBookPath = (newVersionName + ' Atlanta.xlsm')

    workBook = openpyxl.load_workbook(
        fileName, read_only=False, keep_vba=True, keep_links=False)
    newWorkBook = openpyxl.load_workbook(
        newWorkBookPath, read_only=False, keep_vba=True, keep_links=False)

    newWorkBook.save('Backup test')

    # Updates all sheets in the sheetsToBeCopied array

    for sheets in sheetsToBeCopied:

        sh = workBook[sheets]
        mr = sh.max_row
        mc = sh.max_column

        for i in range(1, mr + 1):

            for j in range(1, mc + 1):

                c = sh.cell(row=i, column=j)
                print(c.value)
                print(c)
                print('\n')

                # Checks if its a merged cell, if so skip.
                if(not re.search('MergedCell', str(newWorkBook[sheets].cell(row=i, column=j)))):

                    newWorkBook[sheets].cell(row=i, column=j).value = c.value

    # Event History Management, this is when updating to 9.6

    sh = workBook['EventHistory']
    mr = sh.max_row
    mc = sh.max_column

    for i in range(1, mr + 1):

        for j in range(1, mc + 1):

            c = sh.cell(row=i, column=j)

            print(c.value)
            print(c)
            print('\n')

            # handles the changed columns
            if j == 1:

                newWorkBook['EventHistory'].cell(
                    row=i, column=3).value = c.value

            elif j == 3:

                newWorkBook['EventHistory'].cell(
                    row=i, column=21).value = c.value

            else:

                newWorkBook['EventHistory'].cell(
                    row=i, column=j).value = c.value

    # close and save openpyxl instances
    workBook.close()
    newWorkBook.save('''re.sub('9.3.xlsm', '9.6.xlsm', fileName)''')
    newWorkBook.close()

    '''
    xw.App(visible=False)

    # xlWings section for copying the dashboard over.
    print('made it to xlWings')

    # opens xlwings instances
    xlNewWorkBook = xw.Book(re.sub('9.3.xlsm', '9.6.xlsm', fileName))
    xlMasterWorkBook = xw.Book(newWorkBookPath)
    # deletes and re adds the dashboard

    sht = xlMasterWorkBook.sheets['Dashboard']
    xlNewWorkBook.sheets['Dashboard'].delete()
    sht.api.Copy(Before=xlNewWorkBook.sheets[1].api)

    # changes every cell in the dashboard to that of what it should be

    sh = xlNewWorkBook.sheets['Dashboard']
    sheetRange = sh.used_range
    mr = sheetRange.rows.count
    mc = sheetRange.columns.count

    for i in range(1, mr + 1):

        for j in range(1, mc + 1):

            c = sh.range((i, j))
            print(c.value)
            print(c)
            print('\n')

            newVersionWorkBook.sheets[sheets].range((i, j)).value = c.value

    xlNewWorkBook.save()
    xlMasterWorkBook.close()
    xlNewWorkBook.close()
    '''


def xlWingsTest(fileName, newVersionName, officeType):

    if officeType == 'augusta':

        newWorkBookPath = (newVersionName + ' Augusta.xlsm')
    else:
        newWorkBookPath = (newVersionName + ' Atlanta.xlsm')

    xw.App(visible=False)

    workBook = xw.Book(fileName)
    newWorkBook = xw.Book(newWorkBookPath)
    newWorkBook.save(re.sub('9.3.xlsm', '9.6.xlsm', fileName))
    newVersionWorkBook = xw.Book(re.sub('9.3.xlsm', '9.6.xlsm', fileName))
    newWorkBook.close()

    for sheets in sheetsToBeCopied:

        newWorkBook = sheetCopierXlwings(
            workBook, newWorkBook, sheets, newVersionWorkBook)

    newVersionWorkBook.save()
    # newWorkBook.save('xlWingsTest.xlsm')


def sheetCopierXlwings(workBook, newWorkBook, sheets, newVersionWorkBook):

    if sheets != 'EventHistory':
        '''
        sht = workBook.sheets[sheets]
        sht.api.Copy(Before=newWorkBook.sheets[1].api)
        newWorkBook.sheets[sheets].api.Visible = False
        '''

        sh = workBook.sheets[sheets]
        sheetRange = sh.used_range
        mr = sheetRange.rows.count
        mc = sheetRange.columns.count

        for i in range(1, mr + 1):

            for j in range(1, mc + 1):

                c = sh.range((i, j))
                print(c.value)
                print(c)
                print('\n')

                # Checks if its a merged cell, if so skip.

                newVersionWorkBook.sheets[sheets].range((i, j)).value = c.value

    else:

        sh = workBook.sheets[sheets]
        sheetRange = sh.used_range
        mr = sheetRange.rows.count
        mc = sheetRange.columns.count

        for i in range(1, mr + 1):

            for j in range(1, mc + 1):

                c = sh.range((i, j))
                print(c.value)
                print(c)
                print('\n')

                # handles the changed cell
                if j == 1:

                    newVersionWorkBook.sheets['EventHistory'].range(
                        (i, 3)).value = c.value

                elif j == 3:

                    newVersionWorkBook.sheets['EventHistory'].range(
                        (i, 21)).value = c.value

                else:

                    newVersionWorkBook.sheets[sheets].range(
                        (i, j)).value = c.value


#xlWingsTest(r'F:\ProsperCareFiles\Brooks, Sylvia E Admission 1.11.2018 (0561) 9.3.xlsm',r'F:\ProsperCareFiles\Nurse Admission File 9.6', 'augusta')
updater(r'D:\ProsperCareFiles\Fallen, Tressie Admission 7.12.2018 (8325) 9.3.xlsm',
        r'D:\ProsperCareFiles\Nurse Admission File 9.6', 'atlanta')
