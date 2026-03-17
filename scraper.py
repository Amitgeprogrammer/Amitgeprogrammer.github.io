import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = "https://agenda.exchange"
# Being polite and identifying our bot!
headers = {"User-Agent": "AmitProjectScraper/1.0"}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Grabbing the page title to prove the connection works
    page_title = soup.title.text if soup.title else "No title found"
    
    # Packaging it up with a timestamp
    data = {
        "scraped_data": page_title,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Saving it to the JSON file
    with open("data.json", "w") as f:
        json.dump(data, f)
        
    print("Successfully scraped and saved data!")
    
except Exception as e:
    print(f"Error: {e}")
