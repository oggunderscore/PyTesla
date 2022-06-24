import discord, teslapy, json

tesla = teslapy.Tesla('fujinxyukinko@gmail.com')

with open('tokens.json', 'r') as openfile:
    tokens = json.load(openfile)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

        if message.content.startswith('t! test'):
            vehicles = tesla.vehicle_list()
            print(vehicles[0])
            await message.channel.send(vehicles[0])
            #    print(vehicles[0])

        if message.content.startswith('t! login'):
            if not tesla.authorized:
                await message.channel.send("Use browser to login. Page Not Found will be shown at success.\nOpen this URL: " + tesla.authorization_url())
                #print('Open this URL: ' + tesla.authorization_url())
                tesla.fetch_token(authorization_response=input('Enter URL after authentication: '))
                if tesla.authorized:
                    #print('Successful login.')
                    await message.channel.send('Successful login.')
            else:
                print("You are already logged in")
                await message.channel.send("You are already logged in")

        if "t! logout" in "{0.content}".format(message):
            if tesla.authorized:
                #print('Attempting to logout...')
                await message.channel.send('Attempting to logout...')
                tesla.logout()
                if not tesla.authorized:
                    await message.channel.send('Successful logout')
            if not tesla.authorized:
                #print('Successful logout')
                if isinstance(message.channel, discord.channel.DMChannel) and message.author != self.user:
                    await message.channel.send('Successful logout')


        #print(tesla.vehicle_list()[0])

client = MyClient()
client.run(tokens['discordToken'])
tesla.close()
