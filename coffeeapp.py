import json
import unicodedata
from bs4 import BeautifulSoup
import requests
import re
import os
import datetime
from datetime import datetime

# Set Notion credentials using environment variables
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID") 
headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",  
}

# Fetch the HTML content
def find_string(url, target_string):
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

# Get the interesting coffee information 
def get_coffee_details():
    url = "https://assemblycoffee.co.uk/pages/subscription-the-flavour-index"
    target_strings = ['Producer —', 'Region —', 'Altitude —', 'Variety —', 'Process —' ]
    coffee_dict = {}
    for i in target_strings:
        match = re.search ("(?<=— ).*", unicodedata.normalize("NFKD", find_string(url, i)))
        coffee_dict[i[:-2]] = match.group(0)
    return coffee_dict

# Append an entry to the notion database 
def create_page():
    coffee_dict = get_coffee_details()
    data = {
    "Producer": {"title": [{"text": {"content": coffee_dict["Producer"]}}]},
    "Region": {"rich_text": [{"text": {"content": coffee_dict["Region"]}}]},
    "Altitude": {"rich_text": [{"text": {"content": coffee_dict["Altitude"]}}]},
    "Variety": {"rich_text": [{"text": {"content": coffee_dict["Variety"]}}]},
    "Process": {"rich_text": [{"text": {"content": coffee_dict["Process"]}}]},
    "Month": {"rich_text": [{"text": {"content": datetime.now().strftime("%B")}}]}
    }
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    res = requests.post(create_url, headers=headers, json=payload)
    return res

# Call the fuction
create_page()





