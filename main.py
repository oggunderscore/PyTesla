import discord, teslapy, json, validators

# TODO: KNOWN BUGS LIST
# friend honked my car? he isnt logged on at all possibly because vehicle list is set to 0 which brings the first in the list?

#TODO: QOL LIST
#maybe t! email with no argument returns what email you have it set to for ease of access?

with open('tokens.json', 'r') as openfile:
    tokens = json.load(openfile)

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
            embed.add_field(name="t! debugid", value="tells you your id, email, and token")
            await message.channel.send(embed=embed)

        if message.content.startswith('t! test'):
            with open('emails.json', 'r') as openfile:
                emailDictionary = json.load(openfile)
            vehicles = teslapy.Tesla(emailDictionary[str(client.user.id)]).vehicle_list()
            await message.channel.send(vehicles[0])

        if message.content.startswith('t! login'):
            #check if email is placed
            with open('emails.json', 'r') as openfile:
                emailDictionary = json.load(openfile)
            if str(client.user.id) not in emailDictionary:
                await message.channel.send('Email was not found in directory, Please set it using: t! email [email]')

            # TODO: Shortcut for login, should be globalized? Is this even possible in a safe manner
            tesla = teslapy.Tesla(emailDictionary[str(client.user.id)])

            if not tesla.authorized:
                # Prompt user to open the URL in a browser and enter the code
                await message.channel.send("Use browser to login. Page Not Found will be shown at success.\nOpen this URL then send back the redirected url: " + tesla.authorization_url())
                # Wait for their reply with the url
                def urlcheck(m):
                    if validators.url(m.content):
                        #print('True')
                        return True
                    else:
                        #print('False')
                        return False

                msg = await client.wait_for('message', check=urlcheck)
                if msg:
                    tesla.fetch_token(authorization_response=msg.content)
                    await message.channel.send("URL has been recieved.")
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

        if message.content.startswith('t! debugid'):
            await message.channel.send(client.user.id)
            with open('emails.json', 'r') as openfile:
                emailDictionary = json.load(openfile)
            await message.channel.send(emailDictionary[str(client.user.id)])
            with open('teslatoken.json', 'r') as openfile:
                tokendictionary = json.load(openfile)
            await message.channel.send(tokendictionary[str(client.user.id)])

        if message.content.startswith('t! honk'):
            with open('emails.json', 'r') as openfile:
                emailDictionary = json.load(openfile)
            vehicles = teslapy.Tesla(emailDictionary[str(client.user.id)]).vehicle_list()
            vehicles[0].sync_wake_up()
            vehicles[0].command('HONK_HORN')


client = MyClient()
client.run(tokens['discordToken'])
# TODO: Integrate where on bot close, it will terminate the teslapy session (but this is a per user session?)
# tesla.close()
