import os
import json
import hashlib
import datetime


DATA_DIR = 'data'
META_DIR = os.path.join(DATA_DIR, 'meta')
CITIES_PATH = os.path.join(META_DIR, 'cities.json')
RECORDS_DIR = os.path.join(DATA_DIR, 'records')


def data_load_cities() -> list:

    if not os.path.exists(CITIES_PATH):
        return []
    
    with open(CITIES_PATH, 'r', encoding='utf-8') as file:
        cities = json.load(file)
    return cities

def data_create_city(name: str, population_100k: str) -> bool:

    name = name.lower().strip()
    population_100k = population_100k.strip()
    
    if name == '' or population_100k == '' or not population_100k.isdigit():
        return False

    cities = data_load_cities()
    if name not in [city['name'] for city in cities]:
        cities.append({
            'name': name,
            'population_100k': int(population_100k)
        })
        cities_sorted = sorted(cities, key=lambda c: c['name'])
        with open(CITIES_PATH, 'w', encoding='utf-8') as file:
            json.dump(cities_sorted, file, ensure_ascii=False, indent=4)
        return True
    return False


def hash_city_names(city_names: list) -> str:

    concatenated_names = '_'.join(sorted([name.lower().strip() for name in city_names])).encode('utf-8')
    hash_object = hashlib.sha1(concatenated_names)
    return hash_object.hexdigest()

def data_load_record(city_names: list) -> dict | None:

    if len(city_names) < 2:
        return None

    hash = hash_city_names(city_names)

    record_filename = hash + '.json'
    record_path = os.path.join(RECORDS_DIR, record_filename)

    if not os.path.exists(record_path):
        return None

    with open(record_path, 'r', encoding='utf-8') as file:
        record = json.load(file)
    
    return record

def data_create_record(city_names: list, counts: dict) -> bool:

    if len(city_names) < 2:
        return False

    hash = hash_city_names(city_names)
    timestamp = datetime.datetime.now().isoformat()
    int_counts = {
        row_city: {
            col_city: counts[row_city].get(col_city, 0)
            for col_city in city_names
        }
        for row_city in city_names
    }

    records_filename = hash + '.json'
    records_path = os.path.join(RECORDS_DIR, records_filename)

    records_info = None
    if os.path.exists(records_path):
        with open(records_path, 'r', encoding='utf-8') as file:
            records_info = json.load(file)
    else:
        records_info = {
            'city_names': city_names,
            'records': []
        }

    records_info['records'].append(
        {
            'timestamp': timestamp,
            'counts': int_counts
        }
    )

    with open(records_path, 'w', encoding='utf-8') as file:
        json.dump(records_info, file, ensure_ascii=False, indent=4)
    
    return True