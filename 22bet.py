# %%
import numpy as np 
# import pandas as pd
import time
import json
import logging 
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome



# %%
target_url = "https://22bet33.com/"
# target_url = "https://22bet33.com/en/live/football/"
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get(target_url)

all_competitons = driver.find_element(By.CLASS_NAME, "block_1")



# %%
# for j in all_competitons:
#     print(j.text)

print(all_competitons.text)

# %%
all_competitons

# %%
# football_elem = all_competitons.find_elements(By.XPATH, "//a[@href]")[0]
football_elem = all_competitons.find_elements(By.XPATH, "//a[@title='Football']")
print(football_elem.text)

# %%

driver.close()


