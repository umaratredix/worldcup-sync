import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json

ORIGINAL_API_URL = "https://worldcup26.ir/get/games"
# ⚠️ Apni original Firebase URL yahan check kar lein
FIREBASE_URL = "https://remote-control-test-6b79a-default-rtdb.firebaseio.com/games.json"

def sync_data():
    # 🕵️‍♂️ USER-AGENT TRICK: Server ko lage ke real Chrome browser se request aa rahi hai
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }

    # 🔄 AUTOMATIC RETRY LOGIC: Agar SSL ka jhatka lage toh script khudi 3 dafa naye sire se try karegi
    session = requests.Session()
    retries = Retry(
        total=5, 
        backoff_factor=1, 
        status_forcelist=[500, 502, 503, 504],
        raise_on_status=False
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        print("Fetching data from original API with custom session...")
        # Headers lagane se server request block nahi karega
        response = session.get(ORIGINAL_API_URL, headers=headers, timeout=20)
        
        print(f"Server Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if "games" in data and len(data["games"]) > 0:
                print("Data fetched successfully. Pushing to Firebase...")
                firebase_response = requests.put(FIREBASE_URL, json=data)
                
                if firebase_response.status_code == 200:
                    print("🔥 Firebase Database Updated Successfully!")
                else:
                    print(f"Failed to push to Firebase: {firebase_response.status_code}")
            else:
                print("Alert: Original API returned empty games list.")
        else:
            print(f"Original API server error: {response.status_code}")
            
    except Exception as e:
        print(f"Exception occurred during sync: {str(e)}")

if __name__ == "__main__":
    sync_data()
