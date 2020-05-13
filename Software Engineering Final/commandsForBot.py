import os
import datetime
import smtplib
import django
from django.contrib.auth import authenticate
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from events import models

password = ''


def eventCreation(author, eventName, startTime, endTime, location):

    #dateTime management
    print(author)

    startTime = datetime.datetime.strptime(startTime,"%Y %m %d %H %M")
    endTime = datetime.datetime.strptime(endTime,"%Y %m %d %H %M")
    
    try:
        x = models.Event(name = eventName, creator = models.User.objects.get(discord = author), start_datetime = startTime, end_datetime = endTime, location = location)
        x.save()
    except:
        return ("Error")
   
    y = "Event: " + x.name + " has been created. \nEdit online to add details."

    return y


def linkAccount(userID, usernameGiven, passwordGiven):
    
    x = (authenticate(username = usernameGiven, password = passwordGiven))

    if x is not None:
        x.discord = userID
        x.save()
        return "Account Linked, Remember to relink if you change your discord username"
    else:
        return "Error"


def gameCreation(name, userID, platformName):

    try:
        x = models.Game(name = name, platform = models.Platform.objects.get(name = platformName))
        x.save()
    except:
        return ("Error")

    y = "Game: " + x.name + " has been created."

    return y

# unable to get edit to work
def eventEdit(eventName, fieldName, value, user):

    
    if fieldName == 'start_datetime':

        value = datetime.datetime.strptime(value,"%Y %m %d %H %M")

    elif fieldName == 'end_datetime':

        value = datetime.datetime.strptime(value,"%Y %m %d %H %M")

    
    try:

        r = models.Event.objects.get(name=eventName)

    except:

        y = ("Event: " + eventName + " not found")

        return y

    x = r.creator

    if str(user) == str(x.discord):

        for field in r._meta.get_fields():

            if field.name == fieldName:
                
                print(field)
                print(value)
                r.field = value
                print(field)
                print(value)
                r.save()
                
                return "Value Changed."

        return "Field not found."

    else:

        return("You are not the creator and cannot edit this.")

    return "Unknown Error"

# unable to get edit to work, code here would have looked similar to event edit had it worked
def userEdit(userID, password, field, value):
    return "completed userEdit"

# unable to get edit to work, code here would have looked similar to event edit had it worked
def gameEdit(game, field, value):
    return "completed gameEdit"

def eventDelete(eventName, author):
    
    try:
        r = models.Event.objects.get(name = eventName)
    except:
        return "Error"

    if r.creator == models.User.objects.get(discord = author):

        r.delete()
        return "Event deleted."

    else: 
        
        return "You are not the owner and cannot modify this event."



def userDelete(usernameGiven, passwordGiven):
    
    x = (authenticate(username = usernameGiven, password = passwordGiven))

    if x is not None:
        x.delete()
        return "Account deleted."
    else:
        return "Error"

def gameDelete(game):

    try:
        x = models.Game.objects.get(name = game)
        x.delete()
        return "Game deleted."
    except:
        return "Error"

def getAllEvents():

    returnString = ''

    for item in models.Event.objects.all():

        returnString += item.name + '\n'


    return returnString


def getAllUsers():

    returnString = ''

    for item in models.User.objects.all():

        returnString += item.username + '\n'


    return returnString


def getAllGames():

    returnString = ''

    for item in models.Game.objects.all():

        returnString += item.name + '\n'


    return returnString


def userAddToEvent(event, userID):

    try: 
        try:
            x = models.Event.objects.get(name = event)
        except:
            return "Event Not Found"
        
        try:
            x.attendees.add(models.User.objects.get(discord = userID))
        except:
            return "User not found or account not linked"
        x.save()
        y = "User ", userID," added to ", x.name, "."
        return y
    except:
        return "Error"

def userRemoveFromEvent(event, userID):
    try: 
        x = models.Event.objects.get(name = event)
        x.attendees.remove(models.User.objects.get(discord = userID))
        x.save()
        y = "User ", userID," removed from ", x.name, "."
        return y
    except:
        return "Error"

        
def reminderSystems():

    currentDateTime = datetime.datetime.now().replace(tzinfo=None)
    returnArray = []

    for event in models.Event.objects.all():

        eventTime = event.start_datetime.replace(tzinfo=None)
        
        if (eventTime > currentDateTime) and ((eventTime - currentDateTime).days < 1):


            for attendee in event.attendees.all():
                

                if attendee.email_notifications and attendee.email != '':
                    
                    sendEmail(attendee.email, ("Hi " + attendee.username + ", \n You are being remind of the event, " + event.name + ", at, " + str(event.start_datetime) + "."))
                    
                
                if attendee.discord_notifications:
                    
                    returnArray.append([attendee.discord, event.name, event.start_datetime])
                    
    return returnArray
                

def sendEmail(email, message):

    fromAddr = 'ratemymk18@gmail.com'
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(fromAddr, password)
    server.sendmail(fromAddr, email, message)
    server.quit()


