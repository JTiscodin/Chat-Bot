
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re
import requests
from bs4 import BeautifulSoup

class ActionCaptureEmail(Action):

    def name(self) -> Text:
        return "action_capture_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        email = next(tracker.get_latest_entity_values("email"), None)
        if email and re.match(r"[^@]+@[^@]+\.[^@]+", email):
            dispatcher.utter_message(text=f"Thanks! I've captured your email: {email}")
            return [SlotSet("email", email)]
        else:
            dispatcher.utter_message(text="I didn't understand the email address. Could you please repeat it?")
            return []

class ActionProvideInfo(Action):

    def name(self) -> Text:
        return "action_provide_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Example URL of the website to fetch information from
        url = "http://example.com/services"
        
        # Fetching the webpage content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting relevant information (this part depends on the actual website structure)
        services_info = soup.find('div', class_='services').text
        
        dispatcher.utter_message(text=f"Here is the information about our services: {services_info}")
        return []

class ActionProvidePersonalizedInfo(Action):

    def name(self) -> Text:
        return "action_provide_personalized_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        email = tracker.get_slot('email')
        if email:
            dispatcher.utter_message(text=f"Hi {email.split('@')[0]}, based on your previous interactions, here's some tailored information for you.")
        else:
            dispatcher.utter_message(text="It seems I don't have your email. Could you please provide it for a more personalized experience?")
        
        return []

class ActionFetchWebsiteContent(Action):

    def name(self) -> Text:
        return "action_fetch_website_content"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        query = tracker.latest_message.get('text')
        url = "http://example.com/search"
        params = {'q': query}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract relevant information based on the website's structure
            content = soup.find('div', class_='content').text
            dispatcher.utter_message(text=f"I found this information for you: {content}")
        else:
            dispatcher.utter_message(text="I couldn't retrieve the information at this moment. Please try again later.")
        
        return []
