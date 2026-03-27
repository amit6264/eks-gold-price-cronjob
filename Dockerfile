FROM python:3.9-slim

WORKDIR /app

COPY gold_price_fetcher.py .

RUN pip install requests boto3

CMD ["python", "gold_price_fetcher.py"]
