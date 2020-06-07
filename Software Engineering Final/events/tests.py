from django.test import TestCase
from events.models import Event, User
import datetime
import sys
from pathlib import Path
from events.models import Event

# import module from parent directory
HERE = Path(__file__).parent
sys.path.append(str(HERE / '../../commandsForBot'))
import commandsForBot

class EventWeb(TestCase):
    """Staff members will be able to update (add) new events"""
    def setUp(self):
        User.objects.create_user("test_user",password="p@ssw0rd", discord="test#0000")

    def test_create_event(self):
        name = "test_event"
        start_datetime = datetime.datetime.now()
        end_datetime = start_datetime + datetime.timedelta(days=1)
        creator = User.objects.get(username="test_user")
        
        event = Event.objects.create(name=name, creator=creator, start_datetime=start_datetime, end_datetime=end_datetime)
        self.assertEqual(event.id, Event.objects.get(name=name).id)

    def test_delete_event(self):
        name = "test_event"
        start_datetime = datetime.datetime.now()
        end_datetime = start_datetime + datetime.timedelta(days=1)
        with self.assertRaises(Event.DoesNotExist) as context:
            event = Event.objects.get(name=name)
            print("**********", context)


class EventBot(TestCase):
    """members will be able to join events from discord bot """
    def setUp(self):
        start_datetime = datetime.datetime.now()
        end_datetime = start_datetime + datetime.timedelta(days=1)

        self.user = User.objects.create_user("test_user",password="p@ssw0rd", discord="test#0000")
        self.event = Event.objects.create(name="test_event",creator=User.objects.get(username="test_user"), start_datetime=start_datetime, end_datetime=end_datetime)
    def test_join_event_via_bot(self):
        # make sure event exists
        commandsForBot.userAddToEvent(self.event.name, self.user.discord)
        self.assertIn(self.user,self.event.attendees.all())