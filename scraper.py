import json
from datetime import datetime
from playwright.sync_api import sync_playwright

url = "https://agenda.exchange/profile/amitgep"

def run():
    with sync_playwright() as p:
        # 1. Launch the invisible Chromium browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="AmitProjectScraper/1.0")
        
        print("Loading page and waiting for JavaScript to run...")
        page.goto(url)
        
        try:
            # 2. Wait up to 15 seconds for the site to finish loading the word "Total"
            page.wait_for_selector("text=Total", timeout=15000)
            # Force the robot to wait exactly 3 seconds for the numbers to drop in
            page.wait_for_timeout(3000)
            
            # 3. Locate "Total", jump to its parent container, and grab the sibling container with the number
            total_value = page.locator("span:text-is('Total')").locator("xpath=..").locator("xpath=following-sibling::div").inner_text().strip()
            
            # 4. Do the exact same thing for the P&L
            pnl_value = page.locator("span:text-is('All-Time P&L')").locator("xpath=..").locator("xpath=following-sibling::div").inner_text().strip()
            
        except Exception as e:
            print(f"Could not find elements: {e}")
            total_value = "N/A"
            pnl_value = "N/A"

        print(f"Success! Grabbed Total: {total_value} and P&L: {pnl_value}")
        
        # 5. Save it to your JSON file
        data = {
            "total_portfolio": total_value,
            "all_time_pnl": pnl_value,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open("data.json", "w") as f:
            json.dump(data, f)
            
        browser.close()

if __name__ == "__main__":
    run()
