import machine
import binascii
# Return the unique device id
def get_DeviceId():
    unique_id = machine.unique_id()
    device_id = binascii.hexlify(unique_id).decode('utf-8')
    
    return device_id

def goToDeepSleep():
    machine.deepsleep()

print("IT really was Updated with Gitgub")
