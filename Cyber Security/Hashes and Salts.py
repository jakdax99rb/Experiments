import hashlib
import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# File data getting
with open(os.path.join(ROOT_PATH, 'UID.txt'), 'r') as fileA:

    uidFile = fileA.read()


with open(os.path.join(ROOT_PATH, 'Hash.txt'), 'r') as fileB:

    hashFile = fileB.read()


def computeMD5hash(my_String):
    m = hashlib.md5()
    m.update(my_String.encode('utf-8'))
    return m.hexdigest()


def getHash(password, salt):

    preHash = str(password) + str(salt)
    return computeMD5hash(preHash)


def login(userName, password):

    for i in range(101):

        salt = f"{i:03}"

        if (getHash(password, salt) in hashFile):
            return 'The input password and salt matches the hash value in the database'

    return 'The input password and salt does not match the hash value in the database'


def userEntry():

    userName = str(input('Please enter Username: '))
    password = str(input('Please enter Password: '))
    print('Username: ', userName)
    print('Password: ', password)
    return login(userName, password)


def bruteForce():

    uidList = uidFile.split()
    hashList = hashFile.split()
    saltList = [0]*101
    passList = [0]*101

    titles = ['UID', 'Hashed Password', 'Password', 'Salt']

    for j in range(1001):

        for k in range(101):

            password = f"{j:04}"
            salt = f"{k:03}"
            hashString = getHash(password, salt)

            if (hashString in hashList):

                index = hashList.index(hashString)
                saltList[index] = password
                passList[index] = salt

    # after salt and pass finding

    print('[ UID             Hashed Password          Password  Salt]')

    for v in zip(uidList, hashList, saltList, passList):

        print(v)


print('Question 1 returns hash: ', getHash('0599', '054'), '\n')
print('Question 2')
bruteForce()
print('Question 3\n')
print(userEntry(), '\n')
