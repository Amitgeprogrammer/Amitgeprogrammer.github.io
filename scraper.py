import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Make sure this points to your PUBLIC profile URL, not just the homepage!
url = "https://agenda.exchange/profile/amitgep" 
headers = {"User-Agent": "AmitProjectScraper/1.0"}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 1. Hunt for the "Total" value
    total_label = soup.find('span', string=lambda t: t and 'Total' in t)
    # This goes up to the container, then finds the next box containing the actual number
    total_value = total_label.find_parent('div').find_next_sibling('div').text.strip() if total_label else "N/A"
    
    # 2. Hunt for the "All-Time P&L" value
    pnl_label = soup.find('span', string=lambda t: t and 'All-Time P&L' in t)
    pnl_value = pnl_label.find_parent('div').find_next_sibling('div').text.strip() if pnl_label else "N/A"
    
    # 3. Package both numbers into our JSON file
    data = {
        "total_portfolio": total_value,
        "all_time_pnl": pnl_value,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open("data.json", "w") as f:
        json.dump(data, f)
        
    print(f"Success! Grabbed Total: {total_value} and P&L: {pnl_value}")
    
except Exception as e:
    print(f"Error: {e}")
