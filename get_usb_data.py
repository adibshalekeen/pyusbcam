import usb
import struct
import pickle

info_file = open('info.txt', 'w+')
dev = usb.core.find(find_all=True, bDeviceClass=239)
dev_list = list(dev)
info = ""
cam = dev_list[0]

info += cam._get_full_descriptor_str() + "\n"
cam.set_configuration()

configurations = cam.configurations()

conf = cam.get_active_configuration()
interfaces = conf.interfaces()
info += conf._get_full_descriptor_str() + "\n"

info += "INTERFACES:\n"
for intf in interfaces:
    info += intf._get_full_descriptor_str() + "\n"
    info += intf._str() + "\n"
    info += "ENDPOINTS:\n"
    eps = intf.endpoints()
    for ep in eps:
        info += ep.__str__() + "\n"
info_file.write(info)
info_file.close()

desc = usb.control.get_descriptor(cam, 18, 0x02, 0)
data = struct.unpack(f'<BBHBBBBHHHBBBB', desc)
print(usb.control.get_status(cam))
requestType = usb.util.build_request_type(
    usb.util.CTRL_IN,
    usb.util.CTRL_TYPE_STANDARD,
    usb.util.CTRL_RECIPIENT_DEVICE
)
desc_type = 0x02 << 8

desc = cam.ctrl_transfer(requestType,
                         0x06,
                         wValue = desc_type,
                         data_or_wLength = data[2],\
                         wIndex=0)

output_file = open(f'config_desc', 'wb')
pickle.dump(desc, output_file)
output_file.close()

print(len(desc))
print(desc)
