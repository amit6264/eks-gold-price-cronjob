import requests
import boto3
import os

def main():
    try:
        url = "https://www.goldapi.io/api/XAU/INR"   # INR PRICE ENDPOINT
        headers = {
            "x-access-token": os.getenv("GOLD_API_KEY"),
            "Content-Type": "application/json"
        }

        print("🔍 Fetching Gold Price in INR…")
        response = requests.get(url, headers=headers)
        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print("❌ API Error:", response.text)
            return

        data = response.json()
        print("API Response:", data)

        # GOLDAPI sometimes uses "price", sometimes "price_gram_24k"
        gold_price_inr = data.get("price") or data.get("price_gram_24k")

        if not gold_price_inr:
            print("❌ INR price not found in API response")
            return

        sns = boto3.client("sns", region_name=os.getenv("AWS_REGION"))

        sns.publish(
            TopicArn=os.getenv("SNS_TOPIC_ARN"),
            Subject="Gold Price Update (INR)",
            Message=f"Current Gold Price (INR): ₹{gold_price_inr}"
        )

        print("✅ Email Sent Successfully!")

    except Exception as e:
        print("❌ ERROR:", str(e))


if __name__ == "__main__":
    main()
