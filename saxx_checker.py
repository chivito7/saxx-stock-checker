from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from email.message import EmailMessage
import os
import time

URL = 'https://www.saxxunderwear.com/products/sxpp3jb_bnw?variant=39910770573398'

def send_email():
    msg = EmailMessage()
    msg.set_content("🚨 The item is IN STOCK! Check it now: " + URL)
    msg['Subject'] = "SAXX ITEM IN STOCK"
    msg['From'] = os.environ["GMAIL_ADDRESS"]
    msg['To'] = os.environ["GMAIL_ADDRESS"]
    gmail_app_password = os.environ["GMAIL_PASSWORD"]

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.environ["GMAIL_ADDRESS"], gmail_app_password)
        smtp.send_message(msg)

def check_stock():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Don't open a browser window
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(URL)
    time.sleep(5)  # Give time for JS to load

    try:
        span = driver.find_element(By.CLASS_NAME, 'button-text')
        span_text = span.text.strip().lower()
        print(f"🕵️ Span text: {span_text}")

        if "out of stock" in span_text:
            print("Still sold out...")
        else:
            print("🚨 It's IN STOCK! 🚨 Sending email...")
            send_email()

    except Exception as e:
        print("⚠️ Could not find the stock span:", str(e))
    finally:
        driver.quit()

check_stock()
