from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
driver_path = "./driver/chromedriver.exe" 
opt = Options()
opt.add_argument("--enable-javascript")  
opt.add_argument("--headless")  
opt.add_argument("--disable-infobars") 
opt.add_argument("--disable-extensions") 
opt.add_argument("--disable-blink-features=AutomationControlled")  
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=opt)

from connect import connect
from config import load_config

car_data = {}
cleaned_car_data = {}
def scrap(url):  
    for page in range(1,11):
        b_url = url.format(page)
        driver.get(b_url)
        print(f"Scrapping page {page}: {b_url}")
        col_blocks = driver.find_elements(By.CLASS_NAME, "col-4")
        for car in col_blocks:
            title = car.get_attribute("data-title")
            if not title or not isinstance(title, str):
                continue
            cleaned_title = re.split(r'[^\w\s\d\-\.\/]',title)[0].strip() 
            
            scrapped_price = car.find_element(By.CLASS_NAME, "price")
            if not scrapped_price:
                continue    
            raw_html = scrapped_price.get_attribute("innerHTML")
            new_price_text = raw_html.split("<span")[0].strip()
            cleaned_price = re.sub(r'[^\d]', '', new_price_text)
            
            car_data[title] = new_price_text
            cleaned_car_data[cleaned_title] = cleaned_price
        time.sleep(0.5)
    driver.quit()
    return cleaned_car_data

def push_to_table(data):
    config = load_config()
    conn = connect(config)
    cur = conn.cursor()
    create_table = (
        """
        CREATE TABLE IF NOT EXISTS cartests (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            price INTEGER NOT NULL,
            date_listed DATE DEFAULT CURRENT_DATE
        );
        """)
    cur.execute(create_table)
    try:
        cur.execute("ALTER TABLE cartests ADD CONSTRAINT unique_title UNIQUE (title)") # Allow to set a permission, must run once
    except Exception as e:
        conn.rollback()
        print("A unique title exists. Ignoring error")
    
    for title, price in data.items():
        cur.execute("""
        INSERT INTO cartests (title, price)
        VALUES (%s, %s)
        ON CONFLICT (title) DO UPDATE SET price = EXCLUDED.price
        """, (title,price))
    conn.commit()
    cur.close()
    conn.close()
    print("Push data to Table is done!")
