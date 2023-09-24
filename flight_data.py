

class FlightData:

    def __init__(
            self,
            price:float,
            departure_city:str,
            departure_airport:str,
            departure_date:str,
            arrival_city:str,
            arrival_airport:str,
            return_date:str,
            nights_at_destination:int,
            currency:str,
            booking_link:str
    ):
        self.price = price
        self.departure_city = departure_city
        self.departure_airport = departure_airport
        self.departure_date = departure_date
        self.arrival_city = arrival_city
        self.arrival_airport = arrival_airport
        self.return_date = return_date
        self.nights_at_destination = nights_at_destination
        self.currency = currency
        self.booking_link = booking_link
        



