import requests
from django.http import JsonResponse
from django.shortcuts import render
from evendy.models import Event


def events_list(request):
    url = 'https://app.ticketmaster.com/discovery/v2/events.json?countryCode=DE&apikey=5JpWXsKed1J8wIO2G24nFOOzUa8ZJlCq'
    response = requests.get(url)
    events_data = response.json()

    for event_data in events_data.get('_embedded', {}).get('events', []):
        print(event_data['address'])
        Event.objects.get_or_create(
            title=event_data.get('name', ''),
            date=event_data.get('dates', {}).get('start', {}).get('localDate'),
            time=event_data.get('dates', {}).get('start', {}).get('localTime'),
            place=event_data.get('address', {}).get('line1', '')
            #image=event_data.get('images', [{}])[1].get('url', '')
        )
    #return JsonResponse(events_data)

    events = Event.objects.all()
    return render(request, 'evendy_api/evendy_api.html', {'events': events})



# def oli(request):
#     events = Event.objects.all()
#     return render(request, 'evendy_api.html', {'events': events})
