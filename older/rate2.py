from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Open page
    # page.goto("https://www.monterra.org/rates")
    page.goto("https://consumer.optimalblue.com/FeaturedRates?GUID=8da0b52b-1fef-44da-b650-5a8d169e5761")

    # Click Mortgage Rates button
    page.wait_for_selector("button:has-text('Mortgage Rates')", state="visible", timeout=30000)
    page.locator("button:has-text('Mortgage Rates')").click()
    # Wait for the table
    table = page.wait_for_selector(
        "h2:has-text('Conforming Home Loan Rates') >> xpath=following::table[1]"
    )

    # Extract headers
    headers = table.locator("th").all_text_contents()

    # Extract rows
    rows = table.locator("tr").all()
    data = []

    for row in rows:
        cells = row.locator("td").all_text_contents()
        if cells:
            data.append([c.strip() for c in cells])

    df = pd.DataFrame(data, columns=[h.strip() for h in headers])

    # Save CSV
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("data", exist_ok=True)
    df.to_csv(f"data/{today}_monterra_rates.csv", index=False)

    browser.close()