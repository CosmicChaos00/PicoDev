import urequests as requests
import deviceID
def uploadDevice():
    device_data  = {
        'DeviceID' : deviceID.get_DeviceId(),
        'DeviceName': 'PICO W'
        }
    server_url = 'https://console.cloud.google.com/sql/instances/instancecteserver/studio?project=noted-point-417219'
    try:
        # Send a POST request to the server with the data
        response = requests.post(server_url, json=device_data)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Data sent successfully!")
        else:
            print("Failed to send data. Status code:", response.status_code)
        # Close the response
        response.close()
    except Exception as e:
        print("Error:", e)
        