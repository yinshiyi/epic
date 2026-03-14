from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://consumer.optimalblue.com/FeaturedRates?GUID=8da0b52b-1fef-44da-b650-5a8d169e5761")

    # wait until at least one data row appears
    page.wait_for_selector("tr.datarow", timeout=30000)

    # get the outer HTML of the table containing the rows

    table_html = page.locator("table.ratesTable").nth(0).evaluate("node => node.outerHTML")
    df = pd.read_html(table_html)[0]
    print(df)
    browser.close()