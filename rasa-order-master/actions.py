from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Dict, Text, Any, List

import requests
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction
import json

menu = json.load(open("data.json"))
sub_menu = None
order = []


class order_form(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "order_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["menu", "item", "quantity"]

    def slot_mappings(self):
        return {"menu": self.from_entity(entity="menu",
                                                  intent=["inform"]),
                "item": self.from_entity(entity="item",
                                             intent=["inform"]),
                "quantity": self.from_entity(entity="quantity",
                                             intent=["inform"])
                                             }

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities"""        

        message = "your order is {} {} {}  should i place this order?".format(tracker.get_slot("order"),tracker.get_slot("item"),tracker.get_slot("quantity"))
        global order
        order = []
        
        dispatcher.utter_message(message)

        return [SlotSet("menu",None),SlotSet("size",None),SlotSet("item",None),SlotSet("quantity",None),SlotSet("order",None)]

class find_menu(Action):
    """This action class allows to display buttons for each facility type
    for the user to chose from to fill the facility_type entity slot."""

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "find_menu"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:
        
        buttons = []
        for t in menu.keys():
            
            payload = "/inform{\"menu\": \"" + t + "\"}"

            buttons.append(
                {"title": "{}".format(t.title()),
                 "payload": payload})

        # TODO: update rasa core version for configurable `button_type`
        dispatcher.utter_button_template("utter_greet", buttons, tracker)
        return [SlotSet("menu",None),SlotSet("size",None),SlotSet("item",None),SlotSet("quantity",None),SlotSet("order",None)]
class find_sub_menu(Action):
    """This action class allows to display buttons for each facility type
    for the user to chose from to fill the facility_type entity slot."""

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "find_sub_menu"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:
        if tracker.get_slot("item"):
            return []
        sub_menu_find = tracker.get_slot("menu")
        global order
        
        print(order)
        print(sub_menu_find)
        global sub_menu
        if sub_menu_find is None:
            sub_menu = menu
        else:
            if sub_menu == None:
                sub_menu = menu.get(sub_menu_find,"")
            else:
                if order[-1] != sub_menu_find and order[-1] != None:
                    sub_menu = sub_menu.get(sub_menu_find,"")

        order.append(sub_menu_find)
        buttons = []
        if sub_menu == "":
            dispatcher.utter_message(
                "Sorry, we could not find a {} ".format(sub_menu_find))
            return []
        print(1)
        if isinstance(sub_menu[list(sub_menu.keys())[0]],dict):
            print(2)
            for t in sub_menu.keys():
                print("22")
                payload = "/inform{\"menu\": \"" + t + "\"}"

                buttons.append(
                    {"title": "{}".format(t.title()),
                    "payload": payload})
        else:
            print(3)
            for t in sub_menu.keys():
                print("33")
                payload = "/inform{\"item\": \"" + t + "\"}"

                buttons.append(
                    {"title": "{}".format(t.title()),
                    "payload": payload})
        print(4)
        # TODO: update rasa core version for configurable `button_type`
        dispatcher.utter_button_template("utter_greet", buttons, tracker)
        return [SlotSet("order",order)]
