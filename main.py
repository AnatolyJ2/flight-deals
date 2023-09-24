from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

CITY_IATA_FROM = 'YVR,YXX'

# Flight Prices google sheet instance
data_mngr = DataManager()
cities_data = data_mngr.cities_data

# Update Google sheet iata codes if they are blank
data_mngr.update_destination_iata_code()

flight_search = FlightSearch()
# flight_search.get_flight_data(CITY_IATA_FROM,'YUL')
# exit()
notification_manager = NotificationManager()
for to_city_data in cities_data:

    flight_search_data = flight_search.get_flight_data(CITY_IATA_FROM,to_city_data['iataCode'])

    # Update google sheet with lowest price
    if flight_search_data == None:
        continue
    
    data_mngr.update_all_time_low_price(to_city_data['city'],flight_search_data.price)
    
    if to_city_data['lowestPrice'] > flight_search_data.price:
        #Send sms if price is lower then price in google sheet
        message =  f'🛩️ 🛫{flight_search_data.departure_city}({flight_search_data.departure_airport}) → '
        message += f'🛬{flight_search_data.arrival_city}({flight_search_data.arrival_airport}) '
        message += f'[{flight_search_data.departure_date} to {flight_search_data.return_date} ({flight_search_data.nights_at_destination} nights)]: '
        message += f'${flight_search_data.price}{flight_search_data.currency}\n'
        message += f'{flight_search_data.booking_link}'

        # Send SMS
        notification_manager.send_sms(message)

