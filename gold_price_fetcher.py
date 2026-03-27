import requests
import boto3
import os

def lambda_handler(event, context):
    url = "https://www.goldapi.io/api/XAU/INR"   # INR PRICE
    headers = {
        "x-access-token": os.getenv("GOLD_API_KEY"),
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    gold_price_inr = data["price"]  # price in INR

    sns = boto3.client("sns", region_name=os.getenv("AWS_REGION"))
    sns.publish(
        TopicArn=os.getenv("SNS_TOPIC_ARN"),
        Subject="Gold Price Update (INR)",
        Message=f"Current Gold Price (INR): {gold_price_inr}"
    )

    return {"status": "Success"}
