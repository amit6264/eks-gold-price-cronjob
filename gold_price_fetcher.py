import requests
import boto3
import os

def get_gold_price():
    url = "https://api.metals.live/v1/spot/gold"
    response = requests.get(url)
    price = response.json()[0]['price']
    return price

def send_sns_message(price):
    sns = boto3.client("sns", region_name=os.getenv("AWS_REGION"))
    sns.publish(
        TopicArn=os.getenv("SNS_TOPIC_ARN"),
        Message=f"Today's Gold Price: {price} USD",
        Subject="Gold Price Update"
    )

if __name__ == "__main__":
    price = get_gold_price()
    send_sns_message(price)
    print("SNS Notification Sent!")
