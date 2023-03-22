import requests

API_KEY = "API KEY HERE"

# define the sports to consider
sports = [4]

# define the odds types to consider
odds_types = ["moneyline", "spread"]

# define the minimum profit margin (in percentage) to consider
min_profit_margin_pct = 4

# define the API endpoint and parameters
endpoint = "API SITE HERE"
params = {
    "apiKey": API_KEY,
    "regions": "us",
    "oddsFormat": "american",
    "include": "schedule",
}

# get the data for each sport and odds type
for sport in sports:
    for odds_type in odds_types:
        # add the sport and odds type to the parameters
        params["sport"] = sport
        params["mkt"] = odds_type
        
        # send the request to the API and get the response
        response = requests.get(endpoint, params=params)
        data = response.json()
        
        # check if the response was successful
        if data["success"] == True:
            # get the events and odds
            events = data["data"]
            for event in (events):
                # check if the event has all the required odds
                if all([odds_type in o for o in event["sites"][0]["odds"]]):
                    # get the odds for the first two sites
                    odds1 = event["sites"][0]["odds"][odds_type]
                    odds2 = event["sites"][1]["odds"][odds_type]
                    
                    # calculate the implied probabilities and the profit margin
                    imp_prob1 = 1 / (odds1 / 100 + 1)
                    imp_prob2 = 1 / (odds2 / 100 + 1)
                    profit_margin_pct = 100 / (imp_prob1 + imp_prob2) - 100
                    
                    # check if the profit margin is greater than the minimum required
                    if profit_margin_pct >= min_profit_margin_pct:
                        # display the arbitrage opportunity
                        print(f"Arbitrage opportunity for {event['home_team']} vs {event['away_team']} ({event['commence_time']}) with {odds_type}:")
                        print(f"Site 1: {event['sites'][0]['site_key']} - {odds1}")
                        print(f"Site 2: {event['sites'][1]['site_key']} - {odds2}")
                        print(f"Profit margin: {profit_margin_pct:.2f}%")
                        print("--------------------")
