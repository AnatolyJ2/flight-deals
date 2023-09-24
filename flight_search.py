import requests
# from pprint import pprint
from flight_data import FlightData
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('TEQUILA_API_KEY')
TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
CURRENCY = 'CAD'

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    
    def __init__(self):
        pass
    

    def get_iata_code(self, city_name):
        headers = { 
            "apikey": API_KEY
        }
        params = {
            "term": city_name,
            "location_types": "city"
        }
        resp = requests.get(
            url=f'{TEQUILA_ENDPOINT}/locations/query',
            params=params,
            headers=headers
        )
        resp.raise_for_status()
        return resp.json()['locations'][0]['code']
    

    def get_flight_data(self,city_from_iata,city_to_iata): 

        from datetime import timedelta, datetime as dt
        # Tequila flight search api
        endpoint = 'https://api.tequila.kiwi.com/v2/search'
        url = f'{TEQUILA_ENDPOINT}/v2/search'
        headers = {
            "apikey":API_KEY
        }

        now_dt = dt.now()
        date_from = (now_dt + timedelta(days=7)).strftime('%d/%m/%Y') # Date 2 weeks from today
        date_to = (now_dt + timedelta(weeks=18)).strftime('%d/%m/%Y') # Date 16 weeks from today
        params = {
            "fly_from": city_from_iata,
            "fly_to": city_to_iata,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,    # Minimum stay length
            "nights_in_dst_to": 28,  # Maximum stay length
            "adults": 2,
            "children": 2,
            # "selected_cabins": "M", # M -> Economy
            "max_stopovers": 0, # 0 -> Direct flights only
            "curr": CURRENCY,
            "sort": "price"
        }

        resp = requests.get(url=endpoint,params=params,headers=headers)
        resp.raise_for_status()
        data = resp.json()
        if data['_results'] > 0:
            
            try:
                flight_data = data['data'][0]
            except IndexError:
                print(f'No flights found for {city_to_iata}.')
                return None
            
            flight_out_data = flight_data['route'][0]
            flight_return_data = flight_data['route'][-1]
            price = flight_data['price']
            nights_at_destination = flight_data['nightsInDest']
            departure_date = flight_out_data['local_departure'].split('T')[0]
            departure_city = flight_out_data['cityFrom']
            departure_airport = flight_out_data['flyFrom']
            arrival_date = flight_out_data['local_arrival']
            arrival_city = flight_out_data['cityTo']
            arrival_airport = flight_out_data['flyTo']
            return_date = flight_return_data['local_arrival'].split('T')[0]
            booking_link = flight_data['deep_link']
            
            # print(f'============= {arrival_city} =============')
            # pprint(flight_data)
            out_flight_data = FlightData(
                price=price,
                departure_city=departure_city,
                departure_airport=departure_airport,
                departure_date=departure_date,
                arrival_city=arrival_city,
                arrival_airport=arrival_airport,
                return_date=return_date,
                nights_at_destination = nights_at_destination,
                currency=CURRENCY,
                booking_link=booking_link
            )
            return out_flight_data
