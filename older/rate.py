from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import os

# Set up headless Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)
# Launch the browser and navigate to the webpage
driver.get('https://www.monterra.org/rates')
# https://www.epicpass.com/passes/epic-day-pass.aspx?days=2

# Navigate to the Monterra rates page
# 1. Click the button that loads the table
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Mortgage Rates')]"))
)
print(button)
button.click()

# 2. Wait for the table to load after the click
table = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Conforming Home Loan Rates')]/following::table[1]"))
)

# Parse the table rows
rows = table.find_elements(By.TAG_NAME, "tr")
data = []

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if cells:
        data.append([cell.text.strip() for cell in cells])

# Parse header (from the first row with <th>)
headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]

# Create a DataFrame
df = pd.DataFrame(data, columns=headers)

# Save with today's timestamp
today = datetime.now().strftime("%Y-%m-%d")
if not os.path.exists('data'):
    os.mkdir('data')
df.to_csv(f"data/{today}_monterra_rates.csv", index=False)

# Close the browser
driver.quit()
