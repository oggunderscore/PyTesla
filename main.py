import discord, teslapy, json

# TODO: KNOWN BUGS LIST
# Add bugs here

with open('tokens.json', 'r') as openfile:
    tokens = json.load(openfile)

# TODO: Remove Teslatoken.json as it is not needed anymore, remove references to it as well
with open('teslatoken.json', 'r') as openfile:
    tokendictionary = json.load(openfile)

with open('emails.json', 'r') as openfile:
    emailDictionary = json.load(openfile)

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

        if message.content.startswith('t! help'):
            embed=discord.Embed(title="Tesla Discord bot", description="Welcome to tesla discord bot! this bot will allow you to control your tesla via discord", color=0xFF5733)
            embed.set_author(name="Tesla bot",url="https://github.com/oggunderscore/PyTesla",icon_url="https://tesla-cdn.thron.com/delivery/public/image/tesla/c82315a6-ac99-464a-a753-c26bc0fb647d/bvlatuR/std/1200x628/lhd-model-3-social")
            embed.set_thumbnail(url="https://cdn.mos.cms.futurecdn.net/xz4NVQhHaHShErxar7YLn.jpg")
            embed.add_field(name="t! test", value="pulls up data about your tesla")
            embed.add_field(name="t! login", value="logs you into tesla, must do t! email first")
            embed.add_field(name="t! email [email]", value="binds an email to your discord user id")
            embed.add_field(name="t! logout", value="logs you out")
            embed.add_field(name="t! token", value="binds a token to your discord id")
            embed.add_field(name="t! debugid", value="tells you your id, email, and token")
            await message.channel.send(embed=embed)

        if message.content.startswith('t! test'):
            with open('emails.json', 'r') as openfile:
                emailDictionary = json.load(openfile)
            vehicles = teslapy.Tesla(emailDictionary[str(client.user.id)]).vehicle_list()
            print(vehicles[0])
            await message.channel.send(vehicles[0])
            #    print(vehicles[0])

        if message.content.startswith('t! login'):
            #check if email is placed
            with open('emails.json', 'r') as openfile:
                emailDictionary = json.load(openfile)
            if str(client.user.id) not in emailDictionary:
                await message.channel.send('Email was not found in directory, Please set it using: t! email [email]')

            # TODO: The below code can be removed
            #check if token is placed
            with open('teslatoken.json', 'r') as secondfile:
                tokendictionary = json.load(secondfile)
                
            # TODO: Removed token check because it was causing issues
            #if str(client.user.id) not in tokendictionary:
            #    await message.channel.send('Token was not found in directory, Please set it using: t! token [token]')
            #print("\n\nEmail: " + emailDictionary[str(client.user.id)] + "\tToken: " + tokendictionary[str(client.user.id)] + "\n\n")
            
            # TODO: Shortcut for login, should be globalized? Is this even possible in a safe manner
            tesla = teslapy.Tesla(emailDictionary[str(client.user.id)])
            
            if not tesla.authorized:

                # Prompt user to open the URL in a browser and enter the code
                await message.channel.send("Use browser to login. Page Not Found will be shown at success.\nOpen this URL: " + tesla.authorization_url())
                
                # Wait for their reply with the url
                msg = await client.wait_for('message', check=None)
                # TODO: Implement a check to see if the message is the url using "check" function
                # Refer to: https://discordpy.readthedocs.io/en/latest/api.html#discord.Message

                # Debugging
                # print("\n\nToken: " + msg.content + "\n\n")

                # Use the code to fetch the access token
                tesla.fetch_token(authorization_response=msg.content)

                # TODO: Old code
                #tesla.fetch_token(authorization_response=tokendictionary[str(client.user.id)])
                if tesla.authorized:
                    await message.channel.send('Successful login.')
                else:
                    await message.channel.send('Something went wrong, maybe incorrect email or token type?')
            else:
                await message.channel.send("You are already logged in")

        if message.content.startswith('t! logout'):
            with open('emails.json', 'r') as openfile:
                emailDictionary = json.load(openfile)
            if teslapy.Tesla(emailDictionary[str(client.user.id)]).authorized:
                await message.channel.send('Attempting to logout...')
                with open('emails.json', 'r') as openfile:
                    emailDictionary = json.load(openfile)
                teslapy.Tesla(emailDictionary[str(client.user.id)]).logout()
            if not teslapy.Tesla(emailDictionary[str(client.user.id)]).authorized:
                await message.channel.send('Successful logout')

        if message.content.startswith('t! email'):
            text = message.content
            email = text.split()[-1]
            if(email=="email"):
                await message.channel.send('empty field for email. try: t! email [your email]')
                return
            with open('emails.json', 'r') as openfile:
                emailDictionary = json.load(openfile)
            emailDictionary2={client.user.id:email}
            emailDictionary.update(emailDictionary2)
            json_object= json.dumps(emailDictionary)
            with open("emails.json", "w") as outfile:
                outfile.write(json_object)
            await message.channel.send('Email has been set')


        # TODO: This function can be removed entirely, t! token is not needed with a proper working t! login
        if message.content.startswith('t! token'):
            text = message.content
            token = text.split()[-1]
            with open('emails.json', 'r') as openfile:
                emailDictionary = json.load(openfile)
            if(token=="token"):
                await message.channel.send('Use browser to login. Page Not Found will be shown at success.\nOpen this URL: ' + teslapy.Tesla(emailDictionary[str(client.user.id)]).authorization_url() +' \nThen try: t! token [your token (it should be the url you gain from t! login)]')
                return
            #check if email is placed
            if str(client.user.id) not in emailDictionary:
                await message.channel.send('Email was not found in directory, Its best to set an email before placing the token, Please set it using: t! email [email]')
                return
            #finally do token stuff
            with open('teslatoken.json', 'r') as openfile:
                tokendictionary = json.load(openfile)
            tokendictionary2={client.user.id:token}
            tokendictionary.update(tokendictionary2)
            json_object= json.dumps(tokendictionary)
            with open("teslatoken.json", "w") as outfile:
                outfile.write(json_object)
            await message.channel.send('Token has been set')

        if message.content.startswith('t! debugid'):
            await message.channel.send(client.user.id)
            with open('emails.json', 'r') as openfile:
                emailDictionary = json.load(openfile)
            await message.channel.send(emailDictionary[str(client.user.id)])
            with open('teslatoken.json', 'r') as openfile:
                tokendictionary = json.load(openfile)
            await message.channel.send(tokendictionary[str(client.user.id)])


client = MyClient()
client.run(tokens['discordToken'])
# TODO: Integrate where on bot close, it will terminate the teslapy session (but this is a per user session?)
# tesla.close() 
