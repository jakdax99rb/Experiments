
import os
import smtplib
import sys

#Borrowed from https://github.com/DoctorLai/PyUtils/blob/master/bf.py
def bf(src, left, right, data, idx):
    """
        brainfuck interpreter
        src: source string
        left: start index
        right: ending index
        data: input data string
        idx: start-index of input data string
    """

    outPut = ''

    if len(src) == 0:
        return
    if left < 0:
        left = 0
    if left >= len(src):
        left = len(src) - 1
    if right < 0:
        right = 0
    if right >= len(src):
        right = len(src) - 1
    # tuning machine has infinite array size
    # increase or decrease here accordingly
    arr = [0] * 30000
    ptr = 0
    i = left
    while i <= right:
        s = src[i]
        if s == '>':
            ptr += 1
            # wrap if out of range
            if ptr >= len(arr):
                ptr = 0
        elif s == '<':
            ptr -= 1
            # wrap if out of range
            if ptr < 0:
                ptr = len(arr) - 1
        elif s == '+':
            arr[ptr] += 1
        elif s == '-':
            arr[ptr] -= 1
        elif s == '.':
            outPut += str(chr(arr[ptr]))
        elif s == ',':
            if idx >= 0 and idx < len(data):
                arr[ptr] = ord(data[idx])
                idx += 1
            else:
                arr[ptr] = 0  # out of input
        elif s == '[':
            if arr[ptr] == 0:
                loop = 1
                while loop > 0:
                    i += 1
                    c = src[i]
                    if c == '[':
                        loop += 1
                    elif c == ']':
                        loop -= 1
        elif s == ']':
            loop = 1
            while loop > 0:
                i -= 1
                c = src[i]
                if c == '[':
                    loop -= 1
                elif c == ']':
                    loop += 1
            i -= 1
        i += 1
    return outPut


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'myfile.txt')


def sendPPEmail(toAddr, fromAddr, password):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    ppTxt = open(os.path.join(THIS_FOLDER, 'ppSmol.txt')).read()
    message = ppTxt
    message += '\n\nTranslated: '
    message += bf(ppTxt, 0, len(ppTxt)-1, [], 0)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(fromAddr, password)
    server.sendmail(fromAddr, toAddr, message)
    server.quit()


toAddr = str(input("Enter to address: "))
fromAddr = str(input("Enter from address: "))
password = str(input("Enter Password: "))
sendPPEmail(toAddr, fromAddr, password)
