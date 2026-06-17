import requests
import json

# 1. URL Configurations
ORIGINAL_API_URL = "https://worldcup26.ir/get/games"
# ⚠️ Apni Firebase URL yahan dalein (Aakhri me /games.json lagana zaroori hai)
FIREBASE_URL = "https://YOUR-PROJECT-ID-default-rtdb.firebaseio.com/games.json"

def sync_data():
    try:
        print("Fetching data from original API...")
        response = requests.get(ORIGINAL_API_URL, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # Data validation check taake empty ya corrupt data Firebase me na jaye
            if "games" in data and len(data["games"]) > 0:
                print("Data fetched successfully. Pushing to Firebase...")
                
                # PUT request pure data ko overwrite (replace) kar degi fresh data se
                firebase_response = requests.put(FIREBASE_URL, json=data)
                
                if firebase_response.status_code == 200:
                    print("🔥 Firebase Database Updated Successfully!")
                else:
                    print(f"Failed to push to Firebase: {firebase_response.status_code}")
            else:
                print("Alert: Original API returned empty games list. Skipping update.")
        else:
            print(f"Original API server error: {response.status_code}")
            
    except Exception as e:
        print(f"Exception occurred during sync: {str(e)}")

if __name__ == "__main__":
    sync_data()
