# CoffeeApp

CoffeeApp is a python application intended to fetch information about each months coffee from the [Assembly Coffee Flavour Index subsription](https://assemblycoffee.co.uk/pages/subscription-the-flavour-index), store it in a Notion database, and send an email via Amazon Simple Email Service (SES). The application uses ChatGPT to fetch the following pieces of information:

- Coffee name
- Producer
- Country
- Region
- Farm
- Variety
- Terroir
- Process
- An intersting fact about coffee production in the country (generated by ChatGPT)

The application is intended to be run in AWS Lambda, and in my case runs on a month schedule (on the 11th each month) driven by an Amazon EventBridge Schedule, in line with the coffee subscription cadence. 

You can either use the Terraform provided to set it up from scratch, or feel free to deploy it manually yourself. 

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/juujii/coffeeapp.git
    cd coffeeapp
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Environment Variables

The application requires the following environment variables to be set:

- `NOTION_TOKEN`: Your Notion integration token.
- `NOTION_DATABASE_ID`: The ID of the Notion database where the data will be stored.
- `OPENAI_API_KEY`: Your OpenAI API key.
- `SENDER_EMAIL`: The email address from which notifications will be sent.
- `RECIPIENT_EMAIL`: The recipient email address.

Note that you will need to purchase credit via the [OpenAI Platform](https://platform.openai.com/docs/overview) to make procedural requests. 

## Usage

1. Install [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
2. Setup [AWS CLI access](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
3. Perform a `Terraform Init`
4. Perform a `Terraform Plan` and review the proposed changes. 
5. Perform a `Terraform Apply` to apply the changes.
6. The coffeeapp will execute on the 11th each month at midnight by default. Enjoy!

## License

This project is licensed under the MIT License. See the LICENSE file for details.