import discord, teslapy

from credManager import *

tesla = teslapy.Tesla('oggunderscore@gmail.com')



class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if "t! test" in "{0.content}".format(message):
            vehicles = tesla.vehicle_list()
            print(vehicles[0])
        if "t! login" in "{0.content}".format(message):
            if not tesla.authorized:
                print('Use browser to login. Page Not Found will be shown at success.')
                print('Open this URL: ' + tesla.authorization_url())
                tesla.fetch_token(authorization_response=input('Enter URL after authentication: '))
                if tesla.authorized:
                    print('Successful login.')
            else:
                print("You are already logged in")

                
        if "t! logout" in "{0.content}".format(message):
            if tesla.authorized:
                print('Attempting to logout...')
                tesla.logout()
                
        
        #print(tesla.vehicle_list()[0])

client = MyClient()
client.run('NDU4MDQ3OTcyNjYwMjE1ODQx.Wybsag.fZK4_L0VQ9Zx-Qziv0XOqe3oZ6M')
tesla.close()
