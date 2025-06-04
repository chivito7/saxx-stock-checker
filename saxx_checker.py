import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import os

URL = 'https://www.saxxunderwear.com/products/sxpp3jb_bnw?variant=39910770573398'

def send_email():
    msg = EmailMessage()
    msg.set_content("🚨 The item is IN STOCK! Check it now: https://www.saxxunderwear.com/products/sxpp3jb_bnw?variant=39910770573398")
    msg['Subject'] = "SAXX ITEM IN STOCK"
    msg['From'] = os.environ["GMAIL_ADDRESS"]
    msg['To'] = os.environ["GMAIL_ADDRESS"]

    gmail_app_password = os.environ["GMAIL_PASSWORD"]

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.environ["GMAIL_ADDRESS"], gmail_app_password)
        smtp.send_message(msg)

def check_stock():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Look for the <span class="button-text">Out of Stock</span>
    stock_span = soup.find('span', class_='button-text')

    if stock_span:
        span_text = stock_span.text.strip().lower()
        print(f"🕵️ Found span: '{span_text}'")

        if "out of stock" in span_text:
            print("Still sold out...")
        else:
            print("🚨 It's IN STOCK! 🚨 Sending email...")
            send_email()
    else:
        print("⚠️ Could not find the stock span. Website layout may have changed.")

check_stock()
