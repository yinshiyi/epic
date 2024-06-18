from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, date, time, timezone
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)
#driver = webdriver.Chrome()

# Launch the browser and navigate to the webpage
driver.get('https://www.epicpass.com/pass-results/passes.aspx')
# https://www.epicpass.com/passes/epic-day-pass.aspx?days=2

# Find and click the button
#button = driver.find_element(By.CLASS_NAME, 'pass_configuration__day_selector__button form-control radio radio--custom')
#element = driver.find_element(By.CLASS_NAME,'pass_configuration__day_selector__button form-control radio radio--custom')
#element = driver.find_element(By.CSS_SELECTOR,"label.pass_configuration__day_selector__button.form-control.radio.radio--custom")

#driver.execute_script('arguments[0].setAttribute("aria-checked", "true")', button)

# Find the element
div_elements = driver.find_elements('class name', 'c146__holidaytoggle--v1')
div_element = div_elements[1]
# Scroll to the element
#driver.execute_script("arguments[0].scrollIntoView();", div_element)
driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' });", div_element)

# Click on the element to select the second level of resorts
div_element.click()
# Move up to the parent label element
# label_element = div_element.find_element('xpath', '..')
# label_element.click()

## Wait until OneTrust banner disappears
# button = driver.find_elements(By.CLASS_NAME,"onetrust-close-btn-handler")[1]
# button.click()
# wait = WebDriverWait(driver, 10)
# banner = wait.until(EC.invisibility_of_element_located((By.ID, "onetrust-banner-sdk")))

# Close the browser
# driver.quit()
df = pd.DataFrame(columns=['numofday', 'price'])
days_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'c146__price--v1')))
days = driver.find_elements(By.XPATH,"//label[@manualtoggleid='edpDayToggle']")
for i, day in enumerate(days):
    day.click()
    price_elem = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'c146__price--v1')))
    numofday = day.find_element(By.XPATH, "./div").text
    price = driver.find_elements(By.CLASS_NAME, 'c146__price--v1')[5].text
    df.loc[i] = [numofday, price]

# print all tables indiviually
today = datetime.now()
filename = f"data/{today}_price.csv"
if not os.path.exists('data'):
    os.mkdir('data')
df.to_csv(filename, index=False)


