import string
import random

#generate 24bits values key
def get_key():
    key = ''
    for i in range(0,24):  
        key += str(random.randint(0,1))
    return key

#generate 6 bytes message
def get_message():
    message =''
    for i in range(0,6):
        a = random.randint(48,122)
        message += '{:08b}'.format(a)
    return message

#binary convert to character
def b_c_c(b):
    c = chr(int(b,2))
    return c

#string convert to list and 8bits as a group
def s_to_l(a):
    list1 = list(a)
    step = 8
    list2 = [list1[i:i+step] for i in range(0,len(list1),step)]
    return list2

#list convert to string
def l_to_s(a):
    str1 = ''.join(a)
    return str1

# XOR  encrypt and decrypt 
def encrypt_decrypt(text, key):
    result = ""
    point = 0
    for i in range (len(text)):
        result += str(int(text[i])^int(key[point]))
        point += 1
        if point == len(key):
            point = 0
    return result

#message convert to string   
def printcharacter(a):
    message = ''
    list_message = s_to_l(a)
    for i in range(len(list_message)):
        str1 = l_to_s(list_message[i])
        message += b_c_c(str1)
    return message

# check decrypt
def check_message(original_message,decrypt_message):
    point = 0
    for i in range(len(original_message)):
        if original_message[i] != decrypt_message[i]:
            point -=1
        else:
            point +=1

    if point != len(original_message):
            print('Encrypt & Decrypt System does not work \t \n')
    else:
            print('Encrypt & Decrypt System works properly \t \n')


if __name__ == '__main__':
    message = get_message()
    key = get_key()
    encrypt_message = encrypt_decrypt(message,key)
    decrypt_message = encrypt_decrypt(encrypt_message,key)
    message_character = printcharacter(message)
    encrypt_message_character = printcharacter(encrypt_message)
    decrypt_message_character = printcharacter(decrypt_message)

# print key& original message & encrpyt message & decrypt message
    print('key                        ' +key)
    print('message                    ' + message)
    print('encrypted message (binary) ' + encrypt_message)
    print('decrypted message (binary) ' + decrypt_message)
    print('Message is                 ' + message_character)
    print('Encrypted Message is       ' + encrypt_message_character)
    print('Decrypted Message is       ' + decrypt_message_character)
    print('key length                 ' + str(len(key)) + ' bits')
    print('encrypted message length   ' + str(int(len(encrypt_message)/8)) + '  bytes')
    print('decrypted message length   ' + str(int(len(decrypt_message)/8)) + '  bytes')
# Check decrypt message
    check_message(message,decrypt_message)

