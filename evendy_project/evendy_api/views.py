import requests
from django.shortcuts import render


def events_list():
    events = requests.get('https://app.ticketmaster.com/discovery/v2/events.json?apikey=5JpWXsKed1J8wIO2G24nFOOzUa8ZJlCq')
    print(events.json())



events_list()