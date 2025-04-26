import time
import re
from scrap import scrap, push_to_table
from connect import connect
from config import load_config

url = "https://philkotse.com/used-cars-for-sale/p{}"
dictlist = scrap(url)
filter_car_data = {k: v for k,v in dictlist.items() if len(k) > 10}
push_to_table(filter_car_data)

