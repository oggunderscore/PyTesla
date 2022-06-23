import discord, teslapy, json

tesla = teslapy.Tesla('fujinxyukinko@gmail.com')

with open('tokens.json', 'r') as openfile:
    tokens = json.load(openfile)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

                                        #in order to send clients back messages
#    async def send(*, message):
#        global target_channel
#        await bot.send_message(channel, message)

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

        if "t! test" in "{0.content}".format(message):
            vehicles = tesla.vehicle_list()
            print(vehicles[0])
            if isinstance(message.channel, discord.channel.DMChannel) and message.author != self.user:
                await message.channel.send(vehicles[0])

        if "t! login" in "{0.content}".format(message):
            if not tesla.authorized:
                if isinstance(message.channel, discord.channel.DMChannel) and message.author != self.user:
                    await message.channel.send('Use browser to login. Page Not Found will be shown at success.')
                    await message.channel.send('Open this URL: ' + tesla.authorization_url())
                #print('Open this URL: ' + tesla.authorization_url())
                tesla.fetch_token(authorization_response=input('Enter URL after authentication: '))
                if tesla.authorized:
                    #print('Successful login.')
                    if isinstance(message.channel, discord.channel.DMChannel) and message.author != self.user:
                        await message.channel.send('Successful login.')
            else:
                print("You are already logged in")
                if isinstance(message.channel, discord.channel.DMChannel) and message.author != self.user:
                    await message.channel.send("You are already logged in")

        if "t! logout" in "{0.content}".format(message):
            if tesla.authorized:
                #print('Attempting to logout...')
                if isinstance(message.channel, discord.channel.DMChannel) and message.author != self.user:
                    await message.channel.send('Attempting to logout...')
                tesla.logout()
                if not tesla.authorized:
                    #print('Successful logout')
                    if isinstance(message.channel, discord.channel.DMChannel) and message.author != self.user:
                        await message.channel.send('Successful logout')
            if not tesla.authorized:
                #print('Successful logout')
                if isinstance(message.channel, discord.channel.DMChannel) and message.author != self.user:
                    await message.channel.send('Successful logout')


        #print(tesla.vehicle_list()[0])

#                                                                   another method
#    async def message(ctx, user:discord.member, *, message=None):
#        message = "hello"
#        embed = discord.Embed(title=message)
#        await user.send(enbed=enbed)


client = MyClient()
client.run(tokens['discordToken'])
tesla.close()
