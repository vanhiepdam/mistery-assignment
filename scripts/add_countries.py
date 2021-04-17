# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import os
import sys

import django


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
django.setup()
from locations.models import Country, City


countries = ['Russia', 'UK', 'Ukrain']
cities = {
    'Russia': [
        'Novosibirsk',
        'Nizhny Novgorod',
        'Samara',
        'Omsk',
        'Kazan',
        'Ufa',
        'Chelyabinsk',
    ],
    'UK': ['LONDON', 'Birmingham', 'Leeds', 'Glasgow', 'Sheffield'],
    'Ukrain': [
        'Mykolaiv',
        'Kryvy Rig',
        'Zaporozhye',
        'Odessa',
        'Donetsk',
        'Dnepropetrovsk',
        'Kharkov',
        'KIEV',
    ],
}


def add_cities_to_country(country):
    for country_name in cities:
        if country_name != country.name:
            continue
        for city_name in cities[country_name]:
            print(f"Adding city {city_name} to country {country_name}")
            city, _ = City.objects.get_or_create(name=city_name, country_id=country.id)


def add_countries():
    for country_name in countries:
        print(f"Adding country {country_name}")
        country, _ = Country.objects.get_or_create(name=country_name)
        add_cities_to_country(country)


if __name__ == '__main__':
    add_countries()
