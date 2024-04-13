import requests
from bs4 import BeautifulSoup

def find_string(url, target_string):
    # Fetch HTML content
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch the page")
        return None

    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Search for the target string
    target_element = soup.find(string=lambda text: target_string in str(text))
    if target_element:
        return str(target_element).strip()
    else:
        print(f"Could not find '{target_string}' on the page")
        return None

def get_producer():
    url = "https://assemblycoffee.co.uk/pages/subscription-the-flavour-index"
    target_strings = ['Producers —', 'Region —', 'Altitude —', 'Variety —', 'Process —' ]
    coffee_dict = {}
    for i in target_strings:
        print((find_string(url, i)))
    print(coffee_dict)

get_producer()
