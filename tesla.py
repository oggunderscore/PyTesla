# This file will manage all Tesla functions and data import

import discord, teslapy, json

def loginToTeslaAccount(email): 
    print("\t\t-=-=-= Tesla Login Prompt =-=-=-\n")
    tesla = teslapy.Tesla()
    if not tesla.authorized:
        #print('Open this URL: ' + tesla.authorization_url())
        tesla.fetch_token(authorization_response=input('Enter URL after authentication: '))
            #if tesla.authorized:
                #print('Successful login.')
