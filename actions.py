from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Dict, Text, Any, List

import requests
from rasa_sdk import Action
from rasa_sdk.events import  Form, SlotSet, FollowupAction
from rasa.core.constants import REQUESTED_SLOT
from rasa_core_sdk import ActionExecutionRejection
from rasa_sdk.forms import FormAction
import json 

menu = json.load(open("data.json"))
order = ""
cart = []
fmenu = None
class order_form_type(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "order_form_type"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        if tracker.get_slot('item') == 'pizza':
            return ["item","category" ,"size","quantity","confirmation"]
        else:
            return ["item","category", "quantity","confirmation"]



    def slot_mappings(self):
        return {"item": self.from_entity(entity="item",
                                             intent=["inform_type"]),
                "quantity": self.from_entity(entity="quantity",
                                             intent=["inform"]),
                "category": self.from_entity(entity="category",
                                             intent=["inform_type"]),
                "size": self.from_entity(entity="size",
                                             intent=["inform"]),                
                "confirmation": self.from_entity(entity="confirmation",
                                             intent=["choose"])
                                             }


    def request_next_slot(self, dispatcher, tracker, domain):
        """Send customized message"""    
        global order  
        global fmenu  
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                
                buttons = []        
                if slot == "item":
                    try:
                        fmenu = tracker.get_slot("menu")
                        if fmenu:
                            for t in menu[fmenu].keys():            
                                payload = "/inform{\"item\": \"" + t + "\"}"

                                buttons.append(
                                    {"title": "{}".format(t.title()),
                                    "payload": payload})
                            dispatcher.utter_button_template("utter_ask_{}".format(slot), buttons, tracker)
                        else:
                            for t in menu.keys():            
                                for j in menu[t].keys():
                                    payload = "/inform{\"item\": \"" + j + "\",\"menu\": \"" + t + "\"}"

                                    buttons.append(
                                        {"title": "{}".format(j.title()),
                                        "payload": payload})
                            dispatcher.utter_button_template("utter_ask_{}".format(slot), buttons, tracker)
                            # dispatcher.utter_template("utter_ask_{}".format(slot), tracker)
                    except:
                        dispatcher.utter_template("utter_ask_{}".format(slot), tracker)
                    if fmenu:
                        return [SlotSet("menu", fmenu),SlotSet(REQUESTED_SLOT, slot)]
                    # TODO: update rasa core version for configurable `button_type`
                
                if slot == "category":
                    try:
                        fmenu = tracker.get_slot("menu")
                        item = tracker.get_slot("item")
                        if fmenu and item:
                            for t in menu[fmenu][item].keys():            
                                payload = "/inform{\"category\": \"" + t + "\"}"

                                buttons.append(
                                    {"title": "{}".format(t.title()),
                                    "payload": payload})
                            dispatcher.utter_button_template("utter_ask_{}".format(slot), buttons, tracker)
                        elif item:
                            for i in menu.keys():
                                try:
                                    # dont delete
                                    print(menu[i][item])
                                    fmenu = i 
                                except:
                                    pass                        
                            if fmenu:
                                for t in menu[fmenu][item].keys():            
                                    payload = "/inform{\"category\": \"" + t + "\"}"

                                    buttons.append(
                                        {"title": "{}".format(t.title()),
                                        "payload": payload})
                                dispatcher.utter_button_template("utter_ask_{}".format(slot), buttons, tracker)
                            else:
                                dispatcher.utter_template("utter_ask_{}".format(slot), tracker)
                    except:
                        dispatcher.utter_template("utter_ask_{}".format(slot), tracker)
                    if fmenu:
                        return [SlotSet("menu", fmenu),SlotSet(REQUESTED_SLOT, slot)]
                
                if slot == "size":
                    try: 
                        fmenu = tracker.get_slot("menu")
                        category = tracker.get_slot("category")
                        item = tracker.get_slot("item")
                        if fmenu:
                            for t in menu[fmenu][item][category].keys():            
                                payload = "/inform{\"size\": \"" + t + "\"}"

                                buttons.append(
                                    {"title": "{}".format(t.title()),
                                    "payload": payload})
                            dispatcher.utter_button_template("utter_ask_{}".format(slot), buttons, tracker)
                        else:
                            dispatcher.utter_template("utter_ask_{}".format(slot), tracker)
                    except:
                        dispatcher.utter_template("utter_ask_{}".format(slot), tracker)
                
                if slot == "quantity":
                    dispatcher.utter_template("utter_ask_{}".format(slot), tracker)

                if slot == 'confirmation':    
                    fmenu = tracker.get_slot("menu")
                    order = ""                                        
                    if not tracker.get_slot("order") :
                        price = None                        
                        if fmenu:
                            price  = menu[fmenu]                        
                        for rslot in self.required_slots(tracker)[:-1]:
                            try:                            
                                if rslot != "quantity":
                                    price = price[tracker.get_slot(rslot)]
                                else:
                                    price = int(price) * int(tracker.get_slot(rslot))
                            except:
                                price = None
                            order += tracker.get_slot(rslot)+" "
                        if price:
                            order += " price " + str(price)
                        fmenu = None
                        dispatcher.utter_message("your item is " + order)
                        dispatcher.utter_template("utter_ask_{}".format(slot), tracker)
                        return [SlotSet("order", order),SlotSet(REQUESTED_SLOT, slot)]
                    else:
                        fmenu = None
                        dispatcher.utter_message("your item is " + tracker.get_slot("order"))
                        dispatcher.utter_template("utter_ask_{}".format(slot), tracker)
                        return [SlotSet(REQUESTED_SLOT, slot)]                                                            

                return [SlotSet(REQUESTED_SLOT, slot)]
        return None
        
    def validate(self, dispatcher, tracker, domain):
        # type: (CollectingDispatcher, Tracker, Dict[Text, Any]) -> List[Dict]
        """Extract and validate value of requested slot.

        If nothing was extracted reject execution of the form action.
        Subclass this method to add custom validation and rejection logic
        """
        # extract other slots that were not requested
        # but set by corresponding entity or trigger intent mapping
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))
            if not slot_values:
                tracker.active_form = {}
                tracker.slots["requested_slot"] = None
                print(tracker.latest_message.get('text'))
                if tracker.latest_message.get('text') == "exit" or tracker.latest_message.get('text') == "restart":
                    dispatcher.utter_message(template="utter_greet")
                    return_slots = [Form(None),SlotSet("requested_slot",None)]
                    for slot in tracker.slots:
                        if slot != "cart":
                            return_slots.append(SlotSet(slot, None))
                    return return_slots
                # dispatcher.utter_message(template="utter_something_went_wrong")
        return self.validate_slots(slot_values, dispatcher, tracker, domain)
    
    def validate_quantity(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        try :
            if int(value) > 0 and  int(value) < 20 :
                # validation succeeded, set the value of the "cuisine" slot to value
                return {"quantity": value}
            else:
                dispatcher.utter_message(template="utter_wrong_quantity")
                # validation failed, set this slot to None, meaning the
                # user will be asked for the slot again
                return {"quantity": None}
        except :
            dispatcher.utter_message(template="utter_wrong_quantity")
                # validation failed, set this slot to None, meaning the
                # user will be asked for the slot again
            return {"quantity": None}

    def validate_item(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        global menu
        if value.lower() in list(menu[list(menu.keys())[0]].keys()):
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"item": value}
        else:
            dispatcher.utter_message(template="utter_wrong_item")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"item": None}

    

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities""" 
        global order
        cart = None
        return_slots = []
        if tracker.get_slot("confirmation") == "True" and tracker.get_slot("order") :       
            message = "Item is added to cart \n Anything else you want"
            if not tracker.get_slot("cart"):
                cart = [[tracker.get_slot("order")]]
            else :
                cart = tracker.get_slot("cart") + [[tracker.get_slot("order")]]
            order = ""                        
            return_slots = [Form(None),SlotSet("cart", cart),SlotSet("order", None)]
        else:
            message = "Anything else you want"
            order = ""
            return_slots = [Form(None),SlotSet("order", None)]
        dispatcher.utter_message(message)
        for slot in tracker.slots:
            if slot != "cart":
                return_slots.append(SlotSet(slot, None))
        return return_slots

class place_order(Action):
    """This action class allows to display buttons for each facility type
    for the user to chose from to fill the facility_type entity slot."""

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "place_order"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:
            place_order_item = ""
            total = 0            

            if tracker.get_slot("cart"):
                for i in tracker.get_slot("cart"):
                    place_order_item += i[0] + "\n"
                    if len(i[0].split("price")) > 1:
                        try:
                            total += int(i[0].split("price")[-1])
                        except:
                            print("total error")
                dispatcher.utter_message("your order is " + place_order_item + "Total is " +str(total))
            else:
                dispatcher.utter_message("your cart is empty ")
            
            return [SlotSet("cart", None),Form(None),SlotSet("menu",None),SlotSet("size",None),SlotSet("item",None),SlotSet("quantity",None),SlotSet("order",None),SlotSet("category",None)]


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
        dispatcher.utter_button_template("utter_take_order", buttons, tracker)
        return [SlotSet("menu",None),SlotSet("size",None),SlotSet("item",None),SlotSet("quantity",None),SlotSet("order",None),SlotSet("category",None)]
        
