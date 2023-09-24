# flight-deals

## Initial Setup
- (Optional) Install virtual environment:
```
python3 -m venv .venv
```
- Install dependencies from text file:
```
pip3 install -r requirements.txt
```
- Add ```.env``` file with following variables:
```
TEQUILA_API_KEY = <kiwi api key>
TWILIO_PHONE_NUM = <twilio phone number>
TWILIO_ACCOUNT_SID = <sid>
TWILIO_AUTH_TOKEN = <token>
MY_PHONE_NUM = <your phone number>
SHEETY_PRICES_ENDPOINT = <google sheet endpoint>
```

## Setup API Accounts
### Setup a google sheet that looks something like that:
CITY  | IATA CODE | LOWEST PRICE | ALL TIME LOW PRICE  
"---------------------------------------------------"  
Paris | PAR       | 3500         |  
Tokyo | TYO       | 4000         |  
...

### Use Sheety API to get your flight data from google sheet
Follow the instructions from https://sheety.co/ to link your sheet and get an endpoint

### Twilio API to send SMS
Create an account with Twilio to setup sms messaging: https://www.twilio.com/docs/sms

### Flight search api
Kiwi partners flight search api: https://partners.kiwi.com/
Sign-up is free and you will get a credit for few dollars. No credit card is required.
The documentation can be found here: https://tequila.kiwi.com/portal/docs/tequila_api
