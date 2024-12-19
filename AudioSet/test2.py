import sounddevice as sd
print (sd.query_devices())
# Query the device details
device_info = sd.query_devices(1, 'input')
print(device_info)

