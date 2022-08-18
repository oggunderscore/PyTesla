import discord, teslapy, json

# TODO: TODO / KNOWN BUGS LIST
# Implement refresh token access instead of login access
# Need to add selectedVehicle token attritbute to each discord user to cover for multiple vehicles
#   Store alongside userData.json -- rename userData.json to userData.json?
# friend honked my car? he isnt logged on at all possibly because vehicle list is set to 0 which brings the first in the list?
# Implement a function to consistently refresh cache.json so we have up to date creds?
# Sometimes Vehicle error when sending command; teslapy.VehicleError: Meta slave not woken up within 60 seconds; issue is bot will not read anythiing else during those 60s
#freezes on t! test if not loged in, maybe waiting for timeout


#TODO: QOL LIST
# maybe t! email with no argument returns what email you have it set to for ease of access?

#Done: 
# f string implementation on certain lines
# Renamed emails.json and emailDictionary to userData.json and userData respectively
# Restructured userData.json (formally emails.json) to have {'discordID': {'email': 'email@tesla.com', 'selectedVehicle': '0'}}

with open('tokens.json', 'r') as openfile:
    tokens = json.load(openfile)

with open('userData.json', 'r') as openfile:
    userData = json.load(openfile)

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):

        def getEmail(passid):
            with open('userData.json', 'r') as openfile:
                userData = json.load(openfile)
                return userData[str(passid)]

        print('Message from {0.author}: {0.content}'.format(message))

        if message.content.startswith('t! help'):
            embed=discord.Embed(title="Tesla Discord bot", description="Welcome to tesla discord bot! this bot will allow you to control your tesla via discord", color=0xFF5733)
            embed.set_author(name="Tesla bot",url="https://github.com/oggunderscore/PyTesla",icon_url="https://tesla-cdn.thron.com/delivery/public/image/tesla/c82315a6-ac99-464a-a753-c26bc0fb647d/bvlatuR/std/1200x628/lhd-model-3-social")
            embed.set_thumbnail(url="https://cdn.mos.cms.futurecdn.net/xz4NVQhHaHShErxar7YLn.jpg")
            embed.add_field(name="t! test", value="pulls up data about your tesla")
            embed.add_field(name="t! login", value="logs you into tesla, must do t! email first")
            embed.add_field(name="t! setup", value="setup your account with us")
            embed.add_field(name="t! logout", value="logs you out")
            embed.add_field(name="t! debugid", value="tells you your id, email, and token")
            await message.channel.send(embed=embed)

        if message.content.startswith('t! test'):
            vehicleList = teslapy.Tesla(getEmail(client.user.id)).vehicle_list()
            await message.channel.send(vehicleList[0])
            
        if message.content.startswith('t! vehicles'):
            vehicleList = teslapy.Tesla(getEmail(client.user.id)).vehicle_list()
            #Display the vehicle list to the user
            await message.channel.send(f'Current Vehicle Selected: ')
            for x in vehicleList:
                await message.channel.send(vehvehicleListicles[x])

            

        if message.content.startswith('t! login'):
            #check if email is placed
            with open('userData.json', 'r') as openfile:
                userData = json.load(openfile)
            if str(client.user.id) not in userData:
                await message.channel.send('Email was not found in directory, Please set it using: t! email [email]')

            # TODO: Shortcut for login, should be globalized? Is this even possible in a safe manner
            tesla = teslapy.Tesla(userData[str(client.user.id)])

            if not tesla.authorized:
                # Prompt user to open the URL in a browser and enter the code
                await message.channel.send(f'Click the link below to login. Page Not Found will be shown at success.\n\n {tesla.authorization_url()} \n\nPlease copy the URL and paste it below after successful login')
                # Wait for their reply with the url

                msg = await client.wait_for('message', check=lambda m: m.content.startswith("https://auth.tesla.com/void/callback?code="))
                if msg:
                    await message.channel.send("Attempting to login with provided URL...")
                    tesla.fetch_token(authorization_response=msg.content)
                if tesla.authorized:
                    await message.channel.send('Successful login.')
                    # Find available vehicles and then set default
                    vehicleList = tesla.vehicle_list()
                    if vehicleList is not None: # TODO: Incorrect syntax, fix this

                        with open('userData.json', 'r') as openfile:
                            userData = json.load(openfile)
                        userData2={str(client.user.id)['selectedVehicle']:'0'} # write to as {"458047972660215841": {"email": "oggunderscore@gmail.com", "selectedVehicle": "0"}}
                        userData.update(userData2)
                        json_object= json.dumps(userData)
                        with open("userData.json", "w") as outfile:
                            outfile.write(json_object)
                        
                        #Set default vehicle to 9
                        await message.channel.send(f'Vehicle(s) found, setting current vehicle to <Default Vehicle 0>')
                else:
                    await message.channel.send('Something went wrong, maybe incorrect email or token type?')
            else:
                await message.channel.send("You are already logged in")

        if message.content.startswith('t! logout'):
            with open('userData.json', 'r') as openfile:
                userData = json.load(openfile)
            if teslapy.Tesla(userData[str(client.user.id)]).authorized:
                await message.channel.send('Attempting to logout...')
                with open('userData.json', 'r') as openfile:
                    userData = json.load(openfile)
                teslapy.Tesla(userData[str(client.user.id)]).logout()
            if not teslapy.Tesla(userData[str(client.user.id)]).authorized:
                await message.channel.send('Successful logout')
        # TODO: This function will implement the user setting up their email process and logging in
        if message.content.startswith('t! setup'):
            await message.channel.send('Welcome to the setup process. \n')

            with open('userData.json', 'r') as openfile:
                userData = json.load(openfile)
                if str(client.user.id) in userData:
                    await message.channel.send(f'Your current email is: {userData[str(client.user.id)]}')
                else:
                    await message.channel.send('You are currently do not have a registered email with us.')

            await message.channel.send('Would you like to update or set your email? (Yes or No)\n')
            msg = await client.wait_for('message', check=None)

            if msg.content.lower().startswith('yes'):
                await message.channel.send('Please enter your email: ')
                def emailCheck(message):
                        if "@" in message.content:
                            return True
                        else:
                            # TODO: Add error message for invalid email and prompt to try again?
                            return False
                email = await client.wait_for('message', check=emailCheck)

                with open('userData.json', 'r') as openfile:
                    userData = json.load(openfile)
                userData2={str(client.user.id)['email']:email.content}
                userData.update(userData2)
                json_object= json.dumps(userData)
                with open("userData.json", "w") as outfile:
                    outfile.write(json_object)
                await message.channel.send(f'Email has been successfully updated to: {email.content} \nYou can now login with t! login')

                # TODO: Implement "Would you like to login now?"

            else:
                await message.channel.send('Setup process has been cancelled.')
                return

        if message.content.startswith('t! debugid'):
            await message.channel.send(client.user.id)
            with open('userData.json', 'r') as openfile:
                userData = json.load(openfile)
            await message.channel.send(userData[str(client.user.id)])
            with open('teslatoken.json', 'r') as openfile:
                tokendictionary = json.load(openfile)
            await message.channel.send(tokendictionary[str(client.user.id)])

        if message.content.startswith('t! honk'):
            with open('userData.json', 'r') as openfile:
                userData = json.load(openfile)
            vehicles = teslapy.Tesla(userData[str(client.user.id)]).vehicle_list()
            vehicles[0].sync_wake_up()
            vehicles[0].command('HONK_HORN')

client = MyClient()
client.run(tokens['discordToken'])
# TODO: Integrate where on bot close, it will terminate the teslapy session (but this is a per user session?)
# tesla.close()
