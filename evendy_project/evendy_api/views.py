import requests
from django.core.paginator import Paginator
from django.shortcuts import render
from evendy.models import Event


def events_list(request):
    url = 'https://app.ticketmaster.com/discovery/v2/events.json?countryCode=DE&classificationName=music&apikey=5JpWXsKed1J8wIO2G24nFOOzUa8ZJlCq'
    response = requests.get(url)
    events_data = response.json()

    all_events = []

    total_pages = 10
    # total_pages = events_data['page']['totalPages'] #if you want to see all the results just uncomment this line and comment the line above it

    for page_number in range(total_pages):
        response = requests.get(url, {'page': page_number})
        events_data = response.json()

        for event_data in events_data.get('_embedded', {}).get('events', []):
            if event_data.get('dates', {}).get('status', {}).get('code') != 'cancelled':
                title = event_data.get('name', 'No data')
                date = event_data.get('dates', {}).get('start', {}).get('localDate', 'No data')
                time = event_data.get('dates', {}).get('start', {}).get('localTime', 'No data')

                place = 'no place data'
                for venue_data in event_data.get('_embedded', {}).get('venues', []):
                    place = venue_data.get('city').get('name')

                images = event_data.get('images', {})
                url_4_3 = 'no image data'
                for image in images:
                    if image.get('ratio') == '4_3':
                        url_4_3 = image.get('url')

                event_instance, created = Event.objects.get_or_create(
                    title=title,
                    date=date,
                    time=time,
                    defaults={
                        'place': place,
                        'image': url_4_3
                        }
                    )

                all_events.append(event_instance)

    paginator = Paginator(all_events, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'evendy_api/evendy_api.html', {'page_obj': page_obj})



