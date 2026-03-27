import requests
import boto3
import os

def get_gold_price():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {
        "x-access-token": os.getenv("GOLD_API_KEY"),
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, timeout=10)
    data = response.json()

    return data["price"]   # Based on screenshot

def send_to_sns(price):
    sns_client = boto3.client(
        "sns",
        region_name=os.getenv("AWS_REGION")
    )

    sns_client.publish(
        TopicArn=os.getenv("SNS_TOPIC_ARN"),
        Message=f"Current Gold Price (USD): {price}",
        Subject="Gold Price Update"
    )

if __name__ == "__main__":
    try:
        price = get_gold_price()
        print("Gold Price:", price)
        send_to_sns(price)
        print("SNS Notification Sent.")
    except Exception as e:
        print("Error:", str(e))
