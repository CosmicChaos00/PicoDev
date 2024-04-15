import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import time

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
key_file_path = os.path.join(os.path.dirname(__file__), 'pico-project-key.json')
creds = ServiceAccountCredentials.from_json_keyfile_name(key_file_path, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1vrbrZf9j2jXW-6nyJyDzGXLmlA4ujQJnhvB2Z0ke7cw").sheet1

# MongoDB Data API setup
url = "https://us-east-2.aws.data.mongodb-api.com/app/data-npjph/endpoint/data/v1"
headers = {
    "Content-Type": "application/json",
    "api-key": "UArnVQtRzE1MNZ09LjKQewwhz3Nn9jk8vcrTJzpXghvaxHsMusqcwFrgOn9K729J"
}
params = {
    "dataSource": "Cluster0",
    "database": "TBI",
    "collection": "Player"
}

while True:
    try:
        # Fetch new data from Google Sheets
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        if '_id' in df.columns:
            df.drop(columns=['_id'], inplace=True)

        # Query MongoDB to get existing records
        response = requests.post(f"{url}/action/find", json={
            "collection": params["collection"],
            "database": params["database"],
            "dataSource": params["dataSource"]
        }, headers=headers)

        if response.status_code == 200:
            existing_records = {record['datetime']: record for record in response.json().get('documents', [])}
        else:
            print("Failed to retrieve existing records:", response.status_code)
            existing_records = {}

        # Filter new records to prevent duplicates
        new_documents = [record for record in df.to_dict(orient='records') if record['datetime'] not in existing_records]

        # Insert new data
        if new_documents:
            response = requests.post(f"{url}/action/insertMany", json={
                "collection": params["collection"],
                "database": params["database"],
                "dataSource": params["dataSource"],
                "documents": new_documents
            }, headers=headers)

            if response.status_code == 200:
                print("Inserted new records successfully.")
            else:
                print("Failed to insert new records:", response.json())
        else:
            print("No new records to add.")

        # Wait for some time before the next run
        time.sleep(60)  # Sleep for 60 seconds

    except Exception as e:
        print(f"An error occurred: {e}")
        # Optional: decide if you want to break the loop if an error occurs
        # break
