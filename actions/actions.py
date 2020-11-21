# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk.events import SlotSet, Restarted
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests


#
#
class ActionHelloWorld(Action):
    #
    def name(self) -> Text:
        return "action_hello_world"

    #
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Area_value = tracker.get_slot("location")
        user_id = tracker.sender_id
        user_text = tracker.latest_message['text']
        msg_intent = tracker.latest_message['intent'].get('name')
        msg_confidence = tracker.latest_message['intent'].get("confidence")
        print(f"text:{user_text} intent:{msg_intent} id:{user_id} confidence: {msg_confidence}")
        ##dispatcher.utter_message(str(json_resp))
        try:
            current = requests.get(
                "http://api.weatherstack.com/current?access_key=75c125199af05ff43eec804e5d0094a3&query=" + Area_value).json()

            city = current['location']['name']
            condition = current['current']['weather_descriptions']
            temperature_c = current['current']['temperature']
            humidity = current['current']['humidity']
            wind_mph = current['current']['wind_speed']
            user_text = f"It is currently {condition[0]} in {city} at the moment. The temperature is {temperature_c} degrees, the humidity is {humidity} and the wind speed is {wind_mph} mph "

        except Exception as e:
            pass
        json_resp = {"text": user_text, "intent": msg_intent, "id": user_id, "confidence": msg_confidence}
        dispatcher.utter_message(json_message=json_resp)

        return [Restarted()]
