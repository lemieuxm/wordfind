#!/usr/local/bin/python2.7
# encoding: utf-8
'''
wordfind.data.encrypt -- shortdesc

wordfind.data.encrypt is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2021 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''
import sys

from cryptography.fernet import Fernet


def main():
    key = Fernet.generate_key()
    print("key = %s"%key)
    fernet = Fernet(key)
    message = "This is a test string."
    encMessage = fernet.encrypt(message.encode())
    print("encmessage= %s"%encMessage)
    decMessage = fernet.decrypt(encMessage).decode()
    print("decmessage= %s"%decMessage)
    if message == decMessage:
        print("Success they match!!!")
        

if __name__ == "__main__":
    sys.exit(main())