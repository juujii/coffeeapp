# Intro #

This application pulls the metadata for the current Assembley [flavour index coffee](https://assemblycoffee.co.uk/pages/subscription-the-flavour-index) and stores it into a Notion database. You can use the application coupled with a chron job to automatically store the information on a reoccuring basis. In my case, I use this to have a historical list of coffee that I rate each month.

# Setup # 
## Notion ##

You'll need to create a Notion database (e.g. table) with columns matching the coffee information: 

- Month
- Producer
- Region
- Process
- Variety
- Terroir

Once the database is created, you'll need to [create a token](https://www.notion.so/help/create-integrations-with-the-notion-api) and provide it authorization to edit the database. Once you've done this save the token for the next step. 

## Application ##

The application requires you set the following environment variables:

- NOTION_TOKEN: The token you created in the previous step.
- NOTION_DATABASE_ID: The [ID](https://developers.notion.com/reference/retrieve-a-database) of your Notion database. 

## Automation ##

I use AWS Lambda coupled with EventBridge Scheduler to automate the execution of this each month. You'll need to make some small amendments to the code to include it in the default Lambda function, as well as ensure the environment variables are stored in Lambda. I might make a post on this later. 
