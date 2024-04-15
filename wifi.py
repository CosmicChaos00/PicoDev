import network
import utime
    #i was updated via http
    #visualStudio wrote this
    #this is second update with vscode
def wifi_Login():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks_list = wlan.scan()
    for network_info in networks_list:
        ssid = network_info[0].decode('utf-8')
        print("Available SSID:", ssid)
        
    try:
        with open('wifi.txt', 'r') as file:
            ssid, password = file.readline().strip().split(',')
            
        
        wlan.connect(ssid, password)
        
        # Add a short delay to allow time for connection
        utime.sleep(5)
        
        if wlan.isconnected():
            print("Connected to:", ssid)
        else:
            print("Not connected")

    except Exception as e:
        print("Error:", e)

# Call the function

