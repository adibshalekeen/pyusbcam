import usb
import numpy as np
import time
devs_iter = usb.core.find(find_all=True, bDeviceClass=239)
device_list = list(devs_iter)
cam = device_list[0]
cam.set_configuration()
conf = cam.get_active_configuration()
intfs = conf.interfaces()
index = 0
stream = intfs[2]
eps = stream.endpoints()
ep = eps[0]
print(ep.__str__())
control_intf = intfs[0]
print(stream._get_full_descriptor_str())
# cam.set_interface_altsetting(stream, stream.bAlternateSetting)
prev = time.time()
data = []
while True:
    data = ep.read(31871)
    if data:
        print("FRAME")
        print(time.time() - prev)
        print(len(data))
        print(np.average(data))
        prev = time.time()
