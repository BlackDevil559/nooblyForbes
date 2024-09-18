import requests
import json

# Your API key (replace 'your_token_here' with your actual API token)
stock="AAPL"
# API endpoint URL
url = f"https://finnhub.io/api/v1/company-news?symbol={stock}&from=2023-08-15&to=2023-08-20&token=crlb5ahr01qhc7mk6o10crlb5ahr01qhc7mk6o1g"

# Send GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data from the response
    data = response.json()
    
    # Print the extracted data
    print(json.dumps(data, indent=4))
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
