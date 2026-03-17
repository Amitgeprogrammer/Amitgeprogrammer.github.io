import json
from datetime import datetime
from playwright.sync_api import sync_playwright

# 1. The Squad's URLs
profiles = {
    "Amit": "https://agenda.exchange/profile/amitgep",
    "Shalgon": "https://agenda.exchange/profile/shalgon",
    "Liam": "https://agenda.exchange/profile/liamistockigenda",
    "Bigga": "https://agenda.exchange/profile/bigga"
}

def run():
    scraped_data = [] # We will store everyone's data in this list
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="AgendaLeaderboardScraper/3.0")
        
        # 2. Loop through each friend
        for name, url in profiles.items():
            print(f"Scraping {name}'s profile...")
            page.goto(url)
            
            try:
                page.wait_for_selector("text=Total", timeout=15000)
                page.wait_for_timeout(3000) # The magic 3-second wait
                
                total_value = page.locator("span:text-is('Total')").locator("xpath=..").locator("xpath=following-sibling::div").inner_text().strip()
                pnl_value = page.locator("span:text-is('All-Time P&L')").locator("xpath=..").locator("xpath=following-sibling::div").inner_text().strip()
                
            except Exception as e:
                print(f"Could not grab data for {name}: {e}")
                total_value = "N/A"
                pnl_value = "N/A"
                
            # Add this person's stats to our list
            scraped_data.append({
                "name": name,
                "total_portfolio": total_value,
                "all_time_pnl": pnl_value
            })
            
        # 3. Save the combined list to the JSON file
        final_output = {
            "profiles": scraped_data,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open("data.json", "w") as f:
            json.dump(final_output, f)
            
        browser.close()
        print("Successfully scraped the whole squad!")

if __name__ == "__main__":
    run()
