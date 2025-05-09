import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# Env variables
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LOGIN_URL = "http://94.23.120.156/ints/login"

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def solve_math(text):
    text = text.replace("=", "").replace("?", "").strip()
    try:
        return str(eval(text))
    except:
        return ""

def login_and_navigate():
    driver = setup_driver()
    driver.get(LOGIN_URL)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)

    captcha_label = driver.find_element(By.XPATH, "//label[contains(text(), '=')]").text
    answer = solve_math(captcha_label)
    driver.find_element(By.NAME, 'captcha').send_keys(answer)
    driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".menu-toggle")))
    driver.find_element(By.CSS_SELECTOR, ".menu-toggle").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "SMS Reports")))
    driver.find_element(By.LINK_TEXT, "SMS Reports").click()

    return driver

def send_to_telegram(time_text, number, app, message):
    text = f"""🔔 নতুন OTP পাওয়া গেছে

⏰ সময়: {time_text}
📱 নাম্বার: {number}
💬 অ্যাপ: {app}
✉️ ম্যাসেজ:
```json
{message}
