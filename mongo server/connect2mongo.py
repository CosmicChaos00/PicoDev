import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('pico-project-420216-fa2989878284.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1vrbrZf9j2jXW-6nyJyDzGXLmlA4ujQJnhvB2Z0ke7cw").sheet1
data = sheet.get_all_records()

# Convert data to DataFrame and drop the '_id' column to let MongoDB generate it
df = pd.DataFrame(data)
if '_id' in df.columns:
    df = df.drop(columns=['_id'])  # Remove _id column to avoid duplicates

# MongoDB Data API setup
url = "https://us-east-2.aws.data.mongodb-api.com/app/data-npjph/endpoint/data/v1"
headers = {
    "Content-Type": "application/json",
    "Access-Control-Request-Headers": "*",
    "api-key": "UArnVQtRzE1MNZ09LjKQewwhz3Nn9jk8vcrTJzpXghvaxHsMusqcwFrgOn9K729J"
}

# Database and collection
params = {
    "dataSource": "Cluster0",
    "database": "TBI",
    "collection": "Player"
}

# Convert DataFrame to a dictionary and prepare documents for insertion
documents = df.to_dict(orient='records')

# Insert data
response = requests.post(f"{url}/action/insertMany", json={
    "collection": params["collection"],
    "database": params["database"],
    "dataSource": params["dataSource"],
    "documents": documents
}, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.json())
