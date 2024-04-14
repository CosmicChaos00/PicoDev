import machine
import binascii
# Return the unique device id 4/12/2024 12:27
def get_DeviceId():
    unique_id = machine.unique_id()
    device_id = binascii.hexlify(unique_id).decode('utf-8')
    
    return device_id

def goToDeepSleep():
    machine.deepsleep()

