# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import spacy
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction

from contact_utils import extract_name, add_contact, get_closest_contact
from api_utils import get_currency_rates
from time_utils import analyze_timestring, add_meeting

nlp = spacy.load("pl_spacy_model_morfeusz")

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")
        return []


class ActionSubmitContactForm(Action):

    def name(self) -> Text:
        return "action_submit_contact_form"

    def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slot_name = tracker.get_slot("person")
        email = tracker.get_slot("email")
        name = extract_name(slot_name, nlp)
        data = {"name": name, "email": email}
        add_contact(data)
        confirmation_message = "Dodano kontakt {} o emailu {}".format(name, email)
        dispatcher.utter_message(confirmation_message)
        return [SlotSet("person", name), SlotSet("email", email)]


class ActionSubmitMeetingForm(Action):

    def name(self) -> Text:
        return "action_submit_meeting_form"

    def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("person")
        contact = get_closest_contact(name)
        contact_name = contact["name"]
        time = tracker.get_slot("time")
        meeting_time = str(analyze_timestring(time))
        add_meeting(contact_name, meeting_time)
        confirmation_message = "Dodano spotkanie z {} na datę {}".format(contact_name, meeting_time)
        dispatcher.utter_message(confirmation_message)
        return [SlotSet("person", contact_name), SlotSet("time", meeting_time)]

class ActionGetForex(Action):

    def name(self) -> Text:
        return "action_get_forex"

    def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        rates = get_currency_rates()
        dispatcher.utter_message(text=rates)
        return []


class ActionRecoverContactEmail(Action):

    def name(self) -> Text:
        return "action_recover_contact_email"

    def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("person")
        contact = get_closest_contact(name)
        contact_name = contact["name"]
        contact_email = contact["email"]
        message = "Mail {} to {}".format(contact_name, contact_email)
        dispatcher.utter_message(message)
        return []

