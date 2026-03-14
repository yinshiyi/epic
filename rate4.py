from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    url = "https://consumer.optimalblue.com/FeaturedRates?GUID=8da0b52b-1fef-44da-b650-5a8d169e5761"
    page.goto(url)
    
    # Wait until tables are loaded
    page.wait_for_selector("table.ratesTable tr.datarow", timeout=30000)
    
    tables = page.locator("table.ratesTable")
    all_dfs = []

    for i in range(tables.count()):
        table_html = tables.nth(i).inner_html()
        soup = BeautifulSoup(f"<table>{table_html}</table>", "html.parser")
        
        # Remove AngularJS comments
        for comment in soup.find_all(string=lambda text: isinstance(text, type(soup.Comment))):
            comment.extract()
        
        html_clean = str(soup)
        df = pd.read_html(StringIO(html_clean))[0]
        df["Table"] = i + 1  # optional: keep track of original table
        all_dfs.append(df)
    
    # Merge all tables into a single DataFrame
    merged_df = pd.concat(all_dfs, ignore_index=True)
    
    print(merged_df)
    
    browser.close()