import requests
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from evendy.models import Event


def events_list(request):
    url = 'https://app.ticketmaster.com/discovery/v2/events.json?countryCode=DE&classificationName=music&apikey=5JpWXsKed1J8wIO2G24nFOOzUa8ZJlCq'
    response = requests.get(url)
    events_data = response.json()

    for event_data in events_data['_embedded']['events']:
        if event_data['dates']['status']['code'] != 'cancelled':
            title = event_data['name']
            date = event_data['dates']['start']['localDate']
            time = event_data['dates']['start']['localTime']

            for venue_data in event_data['_embedded']['venues']:
                place = venue_data['city']['name']

            images = event_data['images']

            for image in images:
                if image.get('ratio') == '16_9':
                    url_16_9 = image.get('url')
                    break

            event_instance, created = Event.objects.get_or_create(
                title=title,
                date=date,
                time=time,
                defaults={
                    'place': place,
                    'image': url_16_9
                    }
                )

        events = Event.objects.all()

        paginator = Paginator(events, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, 'evendy_api/evendy_api.html', {'page_obj': page_obj})





