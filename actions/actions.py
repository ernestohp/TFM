# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd
import string
import random

class DefaultFallback(Action):
    def name(self):
        return "my_fallback_action"

    def run(self, dispatcher, tracker, domain):
        response = "Mmmm, no estoy seguro de lo que quieres decirme..." + "\n" + "Me puedes preguntar sobre  \n ● cuarta categoria \n  ● Información generarl \n ● quinta categoria"
        dispatcher.utter_message(text=response)


class ActionDescribe(Action):
    def name(self):
        return "action_respuesta1"

    def run(self, dispatcher, tracker, domain):
        ident = tracker.get_slot("pregunta").upper()
        fecha = tracker.get_slot("fecha")

        if fecha != None:
            inf = describe_information(ident, fecha[0], fecha[1] + ' ' + "23:59:59")
        else:
            inf = describe_information2(ident)

        response = inf
        dispatcher.utter_message(text = response)
        result = response

        return result

class ActionInformacionRuc(Action):
    def name(self):
        return "action_servicio_web_ruc"

    def run(self, dispatcher, tracker, domain):
        N = 20
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

        ident = tracker.get_slot("pregunta").upper()
        fecha = tracker.get_slot("fecha")
        ruc = tracker.get_slot("ruc")

        path = "http://localhost:7000/rucs/" + ident + '/' + fecha + '/' + ruc + '/'  
        dispatcher.utter_message(text="Consultando..." + name, text=path)
        result = dispatcher.msg()

        return result

class ActionUit(Action):
    def name(self):
        return "action_servicio_web_uit"

    def run(self, dispatcher, tracker, domain):
        N = 20
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

        fecha = tracker.get_slot("fecha")
        ruc = tracker.get_slot("ruc")

        path = "http://localhost:7000/uit/" + fecha + '/' + ruc + '/'  
        dispatcher.utter_message(text="Consultando..." + name, text=path)
        result = dispatcher.msg()

        return result

class ActionEstadoDomicilio(Action):
    def name(self):
        return "action_servicio_web_estado_domicilio"

    def run(self, dispatcher, tracker, domain):
        N = 20
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

        fecha = tracker.get_slot("fecha")
        ruc = tracker.get_slot("ruc")

        path = "http://localhost:7000/domicilio/" + fecha + '/' + ruc + '/'  
        dispatcher.utter_message(text="Consultando..." + name, text=path)
        result = dispatcher.msg()

        return result

def describe_information(pregunta, start, end):
    data = pd.read_csv('datasets/respuestas.csv', index_col=0)
    query = data.loc[start  : end ][pregunta]
    return query.describe().apply('{0:.2f}'.format)

def describe_information2(pregunta):
    data = pd.read_csv('datasets/respuestas2.csv', index_col=0)
    query = data[pregunta]
    return query.describe().apply('{0:.2f}'.format)