import requests
import os

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = "196acfa7f31a4aca8c7898cf71d4ae4f"  
headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",  
}

title = "Test Title"
description = "Test Description"
published_date = datetime.now().astimezone(timezone.utc).isoformat()
data = {
    "Producer": {"title": [{"text": {"content": "testProducers1"}}]},
    "Altitude": {"rich_text": [{"text": {"content": "testAltitude1"}}]},
}

def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)
    return res

create_page(data)