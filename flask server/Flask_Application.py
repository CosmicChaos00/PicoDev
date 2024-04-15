from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import  sys
print
app = Flask(__name__)

#set up google sheets credentials

scope = ['https://spreadsheets.google.com/feeds' , 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('pico-project-420216-fa2989878284.json')
client = gspread.authorize(creds)

#specift the google sheet URL
sheet_url = 'https://docs.google.com/spreadsheets/d/1vrbrZf9j2jXW-6nyJyDzGXLmlA4ujQJnhvB2Z0ke7cw/edit?usp=sharing'
sheet = client.open_by_url(sheet_url).sheet1

@app.route('/upload' , methods=['POST'])
def upload_data():
    data = request.json['data']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_with_timestamp = [timestamp] + data
    sheet.append_row(data_with_timestamp)
    return 'Data uploaded successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 3000)