from typing import Any, Text, Dict,Union, List ## Datatypes

from rasa_sdk import Action, Tracker  ##
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ActionReverted, FollowupAction


import re

import MySQLdb

hostname = "35.225.55.69"
username = "rasa_User"
password = "password12"
database = "shopping_db"


class ActionSearch(Action):

    def name(self) -> Text:
        return "action_search"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done
        camera = tracker.get_slot('camera')
        ram = tracker.get_slot('RAM')
        battery = tracker.get_slot('battery')

        dispatcher.utter_message(text='Here are your search results')
        dispatcher.utter_message(text='The features you entered: ' + str(camera) + ", " + str(ram) + ", " + str(battery))
        return []
########################

class ActionShowLatestNews(Action):

    def name(self) -> Text:
        return "action_show_latest_news"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done
        db = MySQLdb.connect(hostname,username,password,database)
        cursor = db.cursor()
        category = tracker.get_slot('category')
        if category == 'phone':
            cursor.execute("SELECT blog_url FROM news WHERE category=%s LIMIT 3",['phone'])
        elif category == 'laptop':
            cursor.execute("SELECT blog_url FROM news WHERE category=%s LIMIT 3",['laptop'])
        news = cursor.fetchall()
        if len(news) != 0:
            for x in news:
                dispatcher.utter_message(text=x[0])
        else:
            dispatcher.utter_message(text='Looks like there isnt any news available.')

        dispatcher.utter_message(template='utter_select_next')
        return []

class ProductSearchForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "product_search_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        if tracker.get_slot('category') == 'phone':
            return ["ram","battery","camera","budget"]
        elif tracker.get_slot('category') == 'laptop':
            return ["ram","battery_backup","storage_capacity","budget"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""


        return {"ram":[self.from_text()],
        "camera":[self.from_text()],
        "battery":[self.from_text()],
        "budget":[self.from_text()],
        "battery_backup":[self.from_text()],
        "storage_capacity":[self.from_text()]
        }


    def validate_battery_backup(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # 8 | Im looking for 8 GB | 8 GB RAM
        # Im looking for ram
        try:
            battery_backup_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            battery_backup_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if battery_backup_int < 50:
            return {"battery_backup":battery_backup_int}
        else:
            dispatcher.utter_message(template="utter_wrong_battery_backup")

            return {"battery_backup":None}

    def validate_storage_capacity(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # 8 | Im looking for 8 GB | 8 GB RAM
        # Im looking for ram
        try:
            storage_capacity_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            storage_capacity_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if storage_capacity_int < 2000:
            return {"storage_capacity":storage_capacity_int}
        else:
            dispatcher.utter_message(template="utter_wrong_storage_capacity")

            return {"storage_capacity":None}

    def validate_ram(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # 8 | Im looking for 8 GB | 8 GB RAM
        # Im looking for ram
        try:
            ram_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            ram_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if ram_int < 50:
            return {"ram":ram_int}
        else:
            dispatcher.utter_message(template="utter_wrong_ram")

            return {"ram":None}

    def validate_camera(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        #
        try:
            camera_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            camera_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if camera_int < 150:
            return {"camera":camera_int}
        else:
            dispatcher.utter_message(template="utter_wrong_camera")

            return {"camera":None}

    def validate_budget(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # i want the ram
        try:
            budget_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            budget_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if budget_int < 4000:
            return {"budget":budget_int}
        else:
            dispatcher.utter_message(template="utter_wrong_budget")

            return {"budget":None}

    def validate_battery(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        #
        try:
            battery_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            battery_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if battery_int < 8000:
            return {"battery":battery_int}
        else:
            dispatcher.utter_message(template="utter_wrong_battery")

            return {"battery":None}


    
    # USED FOR DOCS: do not rename without updating in docs
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        if tracker.get_slot('category') == 'phone':
            dispatcher.utter_message(text="Please find your searched items here: Phones..")

        elif tracker.get_slot('category') == 'laptop':
            dispatcher.utter_message(text="Please find your searched items here: Laptops..")
        category = tracker.get_slot('category')
        #Open a database connection
        db = MySQLdb.connect(hostname,username,password,database)
        ram = tracker.get_slot('ram')
        battery = tracker.get_slot('battery')
        battery_backup = tracker.get_slot('battery_backup')
        storage_capacity = tracker.get_slot('storage_capacity')
        camera = tracker.get_slot('camera')
        budget = tracker.get_slot('budget')

        #prepare a cursor object
        cursor = db.cursor()
        if category == 'phone':
            cursor.execute("SELECT product_url FROM products WHERE ram >= %s AND back_camera_megapixel >= %s AND \
                battery_mah >= %s AND price_usd <= %s AND category= %s", [int(ram),\
                int(camera), int(battery), int(budget), 'phone'])
        elif category == 'laptop':
            cursor.execute("SELECT product_url FROM products WHERE ram >= %s AND storage >= %s AND \
                battery_backup >= %s AND price_usd <= %s AND category= %s", [int(ram),\
                int(storage), int(battery_backup), int(budget), 'laptop'])
        products = cursor.fetchall()
        if len(products) != 0:
            for x in products:
                dispatcher.utter_message(text=x[0])
        else:
            dispatcher.utter_message(text="Looks like there aren't any products that match your search.")       
        dispatcher.utter_message(template='utter_select_next')

        return [SlotSet('ram',None),SlotSet('camera',None),SlotSet('battery_backup',None),\
        SlotSet('battery',None),SlotSet('storage_capacity',None),SlotSet('budget',None)]

class MyFallback(Action):

    def name(self) -> Text:
        return "action_my_fallback"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_fallback")

        return []

class YourResidence(Action):

    def name(self) -> Text:
        return "action_your_residence"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done
        dispatcher.utter_message(template="utter_residence")

        return [UserUtteranceReverted(),FollowupAction(tracker.active_form.get('name'))]