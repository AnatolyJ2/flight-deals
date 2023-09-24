import requests
import os
from notification_manager import NotificationManager
from dotenv import load_dotenv

load_dotenv()

SHEETY_PRICES_ENDPOINT = os.getenv('SHEETY_PRICES_ENDPOINT')

# add city IATA code to google sheet
class DataManager:
    
    def __init__(self):
        self.cities_data = self.get_cities_data()

    def get_cities_data(self):
        resp = requests.get(url=SHEETY_PRICES_ENDPOINT)
        resp.raise_for_status()
        self.cities_data = resp.json()['prices']
        return resp.json()['prices']
        
    def update_destination_iata_code(self):

        from flight_search import FlightSearch
        flight_search = FlightSearch()

        for city_data in self.cities_data :
            if city_data['iataCode'] == "":
                city_iata_code = flight_search.get_iata_code(city_data['city'])   
                city_data['iataCode'] = city_iata_code

                params={
                    "price": city_data
                }
                resp = requests.put(
                    url=f'{SHEETY_PRICES_ENDPOINT}/{city_data["id"]}',json=params
                )

                if resp.status_code != 200:
                    print(f'IATA Code for {city_data["city"]} FAILED to update!!!')
                else:
                    print(f'IATA Code for {city_data["city"]} was updated')

    
    def update_all_time_low_price(self,city,price:float) -> None:

        try:
            city_data = next(data for data in self.cities_data if data['city']==city)
        except StopIteration:
            return

        hasCurrAllTimeLowPrice = True
        isNewAllTimeLowPrice = False
        try:
            allCurrTimeLowPrice = city_data['allTimeLowPrice']
        except KeyError:
            isNewAllTimeLowPrice = True
            hasCurrAllTimeLowPrice = False

        if hasCurrAllTimeLowPrice and allCurrTimeLowPrice > price:
            isNewAllTimeLowPrice = True

        if isNewAllTimeLowPrice:
            city_data['allTimeLowPrice'] = price
            params={
                    "price": city_data
            }
            resp = requests.put(
                url=f'{SHEETY_PRICES_ENDPOINT}/{city_data["id"]}',json=params
            )
            if resp.status_code != 200:
                print(f'All Time Low Price for {city} FAILED to update!!!')
            else:
                # Send SMS
                notification_manager = NotificationManager()
                notification_manager.send_sms(f'All Time Low Price for {city} was updated')
                # print(f'All Time Low Price for {city} was updated')

            


