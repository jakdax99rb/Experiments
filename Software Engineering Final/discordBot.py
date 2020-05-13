# This file will store what runs the bot then will call other py functions
# Message returns to the user are going to be in the form of return strings from the commandsForBot.py file.
# For reminders we will need an async loop to check times against the database of events

import commandsForBot
import discord
import asyncio


token = ''

class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.bg_task = self.loop.create_task(self.reminders())
    
    async def on_ready(self):
        
        print('We have logged in as {0.user}'.format(self))

    async def reminders(self):
        
        await self.wait_until_ready()
        channel = self.get_channel(684523075152117874)

        while not self.is_closed():

            returnedArrays = commandsForBot.reminderSystems()
            messageString = ''

            if (len(returnedArrays) > 0):  

                for grouping in returnedArrays:
                    
                    userId = int(grouping[0])
                    eventName = grouping[1]
                    eventStart = str(grouping[2])
                    
                    messageString = messageString + '\n' + str(client.get_user(userId).mention + ", You are being reminded of " + str(eventName) + ", at " + str(eventStart) + ".")

            await channel.send(messageString)
            await asyncio.sleep(82500)


    async def on_message(self, message):
        args = message.content.split(',')
        args = [element.strip() for element in args]
        user = message.author.id
        mention = message.author.mention
        

        # checks if sender is the bot itself, if so ignore
        if message.author == self.user:

            return

        # help message
        if message.content.startswith('$help'):


            # populate this with documentation on all of the below commands. Try to use discords embed system to create a nice looking message.

            helpEmbed = discord.Embed(type='rich', title='Command List',
                                    description='A list of commands and their arguments. Use a comma to seperate arguments and commands. Ex. $linkAccount,username2,stuffandthings')
            helpEmbed.add_field(
                name='$linkAccount', value='PM the bot to use the command \narguments username password')
            helpEmbed.add_field(name='$createEvent',
                                value='arguments eventName, startTime (year month day hour minute all in numbers) , endTime (year month day hour minute all in numbers), location. Edit online to add details.', inline=True)
            helpEmbed.add_field(name='$createGame',
                                value='arguments gameName, platformName', inline=True)
            helpEmbed.add_field(name='$editEvent',
                                value='Only the event owner can edit \narguments eventName fieldName value')
            helpEmbed.add_field(
                name='$editUser', value='PM the bot to use the command \narguments userName password fieldName value', inline=True)
            helpEmbed.add_field(
                name='$editGame', value='arguments gameName, fieldName, value', inline=True)
            helpEmbed.add_field(
                name='$deleteEvent', value='Only the event owner can delete\narguments eventName')
            helpEmbed.add_field(name='$deleteUser',
                                value='PM the bot to use this command\narguments userName, passWord', inline=True)
            helpEmbed.add_field(name='$deleteGame',
                                value='arguments gameName', inline=True)
            helpEmbed.add_field(
                name='$addUserToEvent', value='Add yourself to event\narguments eventName')
            helpEmbed.add_field(name='$removeUserFromEvent',
                                value='Remove yourself from event\narguments eventName', inline=True)
            helpEmbed.add_field(name='$getAllEvents',
                                value='Display all events\n')
            helpEmbed.add_field(name='$getAllUsers',
                                value='Display all users\n', inline=True)
            helpEmbed.add_field(name='$getAllGames',
                                value='Display all games\n', inline=True)


            await message.channel.send(embed=helpEmbed)

            # Link Account
        if message.content.startswith('$linkAccount'):

            if str(message.channel.type) == 'private':

                if len(args) < 3:

                    await message.channel.send(mention + ", you are missing arguments. $help for commands")

                else:

                    await message.channel.send(str(commandsForBot.linkAccount(user, args[1], args[2])))

            else:

                await message.channel.send(mention + ", This command only works in private messages. $help for commands")

        # arguments need to be input in a specific order seperated by spaces for simplicity sake.
        # Event Creation, user will just pass name of event and will use $eventEdit later to add more.
        if message.content.startswith('$createEvent'):


            if len(args) < 2:

                await message.channel.send(mention + ", you are missing arguments. $help for commands")

            else:

                await message.channel.send(str(commandsForBot.eventCreation(user, args[1], args[2], args[3], args[4])))

        # Game Creation
        if message.content.startswith('$createGame'):


            if len(args) < 2:

                await message.channel.send(mention + ", you are missing arguments. $help for commands")

            else:

                await message.channel.send(str(commandsForBot.gameCreation(args[1], user, args[2])))

        # Event Edit
        if message.content.startswith('$editEvent'):


            if len(args) < 4:

                await message.channel.send(mention + ", you are missing arguments. $help for commands")

            else:

                await message.channel.send(str(commandsForBot.eventEdit(args[1], args[2], args[3], user)))

        # User Edit
        if message.content.startswith('$editUser'):

            if str(message.channel.type) == 'private':



                if len(args) < 4:

                    await message.channel.send(mention + ", you are missing arguments. $help for commands")

                else:

                    await message.channel.send(str(commandsForBot.userEdit(user, args[1], args[2])))

            else:

                await message.channel.send(mention + ", This command only works in private messages. $help for commands")

        # Game Edit
        if message.content.startswith('$editGame'):


            if len(args) < 4:

                await message.channel.send(mention + ", you are missing arguments. $help for commands")

            else:

                await message.channel.send(str(commandsForBot.gameEdit(args[1], args[2], args[3], user)))

        # Event Delete
        if message.content.startswith('$deleteEvent'):


            if len(args) < 2:

                await message.channel.send(mention + ", you are missing arguments. $help for commands")

            else:

                await message.channel.send(str(commandsForBot.eventDelete(args[1], user)))

        # User Delete
        if message.content.startswith('$deleteUser'):


            if len(args) < 2:

                await message.channel.send(mention + ", you are missing arguments. $help for commands")

            else:

                await message.channel.send(str(commandsForBot.userDelete(args[1], user)))

        # Game Delete
        if message.content.startswith('$deleteGame'):


            if len(args) < 2:

                await message.channel.send(mention + ", you are missing arguments. $help for commands")

            else:

                await message.channel.send(str(commandsForBot.gameDelete(args[1])))

        # Add user to event, takes the authors user
        if message.content.startswith('$addUserToEvent'):


            if len(args) < 2:

                await message.channel.send(mention + ", you are missing arguments. $help for commands")

            else:

                await message.channel.send(str(commandsForBot.userAddToEvent(args[1], user)))

        # remove user from event, takes the authors user
        if message.content.startswith('$removeUserFromEvent'):


            if len(args) < 2:

                await message.channel.send(mention + ", you are missing arguments. $help for commands")

            else:

                await message.channel.send(str(commandsForBot.userRemoveFromEvent(args[1], user)))

        if message.content.startswith('$getAllEvents'):

            await message.channel.send(str(commandsForBot.getAllEvents()))

        if message.content.startswith('$getAllUsers'):

            await message.channel.send(str(commandsForBot.getAllUsers()))

        if message.content.startswith('$getAllGames'):

            await message.channel.send(str(commandsForBot.getAllGames()))

    

if __name__ == '__main__':
    client = MyClient()
    client.run(token)
