import os
import requests
import json
from openai import OpenAI
from notion_client import Client
from datetime import datetime
import boto3

# Initialize variables and client
url = "https://assemblycoffee.co.uk/pages/subscription-the-flavour-index"
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ses_client = boto3.client('ses', region_name='eu-west-2')
sender_email = os.environ.get("SENDER_EMAIL")
recipient_email_1 = os.environ.get("RECIPIENT_EMAIL_1")
recipient_email_2 = os.environ.get("RECIPIENT_EMAIL_2")

# Error handling for environment variables
if not NOTION_TOKEN:
	print("FAILURE: NOTION_TOKEN environment variable is not set.")
	exit(1)
if not DATABASE_ID:
	print("FAILURE: NOTION_DATABASE_ID environment variable is not set.")
	exit(1)
if not OPENAI_API_KEY:
	print("FAILURE: OPENAI_API_KEY environment variable is not set.")
	exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)
notion = Client(auth=NOTION_TOKEN)

# Fetch the HTML content and craft prompt
def get_html_content(url):
	try:
		response = requests.get(url)
		response.raise_for_status()
		return f"Find the following in this html object: name (excluding country), country, producer, farm, region, variety, terroir, process. I'd also like you to summarise an interesting fact about coffee production in this country around 150 words. Add this to the same dictionary and use fact as the key. If you can't find any of the pieces of information just pass <unknown>. Only return the dictionary containing this information without the code block:\n\n{response.text}"
	except requests.exceptions.RequestException as e:
		print(f"FAILURE: Error fetching the URL: {e}")
		exit(1)

# Send the request to the OpenAI API
def get_coffee_info():
	prompt = get_html_content(url)
	try:
		response = client.chat.completions.create(
			model="gpt-4o-mini",
			messages=[
				{"role": "user", "content": prompt}
			]
		)
		coffee_dict = response.choices[0].message.content.strip()
		return json.loads(coffee_dict)
	except Exception as e:
		print(f"Error processing the OpenAI API response: {e}")
		exit(1)

# Prepare the data for Notion
def publish_to_notion(database_id):
	coffee_info = get_coffee_info()
	notion_data = {
		"parent": {"database_id": database_id},
		"properties": {
			"Name": {"rich_text": [{"text": {"content": coffee_info.get('name', '')}}]},
			"Country": {"rich_text": [{"text": {"content": coffee_info.get('country', '')}}]},
			"Producer": {"title": [{"text": {"content": coffee_info.get('producer', '')}}]},
			"Farm": {"rich_text": [{"text": {"content": coffee_info.get('farm', '')}}]},
			"Region": {"rich_text": [{"text": {"content": coffee_info.get('region', '')}}]},
			"Variety": {"rich_text": [{"text": {"content": coffee_info.get('variety', '')}}]},
			"Terroir": {"rich_text": [{"text": {"content": coffee_info.get('terroir', '')}}]},
			"Process": {"rich_text": [{"text": {"content": coffee_info.get('process', '')}}]},
			"Fact": {"rich_text": [{"text": {"content": coffee_info.get('fact', '')}}]},
			"Month": {"rich_text": [{"text": {"content": datetime.now().strftime("%B")}}]}
		}
	}
	try:
		# Add the data to the Notion database
		notion.pages.create(**notion_data)
		print("SUCCESS: Data added to Notion database.")
		# Send the email
		ses_client.send_email(
			Destination={
				'ToAddresses': [
					recipient_email_1,
					recipient_email_2
				],
			},
			Message={
				'Body': {
					'Html': {
						'Charset': "UTF-8",
						'Data': f"""
						<html>
						<head></head>
						<body>
							<p><strong>Name:</strong> {coffee_info.get('name', 'N/A')}</p>
							<p><strong>Producer:</strong> {coffee_info.get('producer', 'N/A')}</p>
							<p><strong>Country:</strong> {coffee_info.get('country', 'N/A')}</p>
							<p><strong>Region:</strong> {coffee_info.get('region', 'N/A')}</p>
							<p><strong>Farm:</strong> {coffee_info.get('farm', 'N/A')}</p>
							<p><strong>Variety:</strong> {coffee_info.get('variety', 'N/A')}</p>
							<p><strong>Terroir:</strong> {coffee_info.get('terroir', 'N/A')}</p>
							<p><strong>Process:</strong> {coffee_info.get('process', 'N/A')}</p>
							<p>{coffee_info.get('fact', 'N/A')}</p>
						</body>
						</html>
						"""
					}
				},
				'Subject': {
					'Charset': "UTF-8",
					'Data': f"{datetime.now().strftime('%B')} Coffee: {coffee_info.get('name', 'N/A')} from {coffee_info.get('producer', 'N/A')}"
				}
			},
			Source=sender_email
		)
		print("SUCCESS: Email sent.")
	except Exception as e:
		print(f"FAILURE: Error adding data to Notion: {e}")
		exit(1)
        
# Call the function
publish_to_notion(DATABASE_ID)