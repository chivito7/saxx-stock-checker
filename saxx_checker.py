import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.message import EmailMessage
import os

URL = 'https://www.saxxunderwear.com/products/sxpp3jb_bnw?variant=39910770573398'

def send_email(stock_status):
    msg = EmailMessage()
    msg.set_content(f"🚨 SAXX item status: {stock_status}. Check here: {URL}")
    msg['Subject'] = "SAXX Stock Alert"
    msg['From'] = os.environ['GMAIL_ADDRESS']
    msg['To'] = os.environ['GMAIL_ADDRESS']

    gmail_app_password = os.environ['GMAIL_PASSWORD']

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.environ['GMAIL_ADDRESS'], gmail_app_password)
        smtp.send_message(msg)

def check_stock():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    if "Sold Out" in soup.text or "Out of stock" in soup.text:
        stock_status = "NOT in stock"
        print("Still sold out...")
    else:
        stock_status = "IN STOCK"
        print("🚨 It's IN STOCK! 🚨")

    send_email(stock_status)

check_stock()
