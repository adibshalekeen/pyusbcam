'''This module contains classes representing standard USB descriptors'''
class Descriptor:
    def __init__(self, data):
        self._length = data[0]
        self._descriptor_type = data[1]

    @property
    def bLength(self):
        '''The length of the descriptor'''
        return self._length
    
    @property
    def bDescriptorType (self):
        '''The type code of the descriptor'''
        return self._descriptor_type

class DeviceDescriptor(Descriptor):
    '''Class representing USB device descriptors'''

    def __init__(self, data):
        super().__init__(data)
        self._usb_version = data[2:4]
        self._device_class = data[4]
        self._device_sub_class = data[5]
        self._device_protocol = data[6]
        self._max_packet_size = data[7]
        self._vid = data[8:10]
        self._pid = data[10:12]
        self._device_release_code = data[12:14]
        self._mid_str_index = data[14]
        self._product_name_index = data[15]
        self._serial_number = data[16]
        self._num_configs = data[17]
    
    @property
    def bcdUSB(self):
        '''USB Specification version'''
        self._usb_version
    
    @property
    def bDeviceClass(self):
        '''Class ID of the device'''
        return self._device_class
    
    @property
    def bDeviceSubClass(self):
        '''Sub class ID of the device'''
        return self._device_sub_class
    
    @property
    def bDeviceProtocol(self):
        '''Protocol for communication with this device'''
        return self._device_protocol

    @property
    def bMaxPacketSize(self):
        '''Maximum packet size of the control interface'''
        return self._max_packet_size
    
    @property
    def idVendor(self):
        '''Vendor ID of the device'''
        return self._vid
    
    @property
    def idProduct (self):
        '''Product ID of the device'''
        return self._pid
    
    @property
    def bcdDevice(self):
        '''Product version of the device (Manufacturer controlled)'''
        return self._device_release_code
    
    @property
    def iManufacturer(self):
        '''Index of the manufacturer ID string descriptor'''
        return self._mid_str_index
    
    @property
    def iProduct(self):
        '''Index of the product name string descriptor'''
        return self._product_name_index
    
    @property
    def bNumConfigurations(self):
        '''The number of configurations this device supports'''
        return self._num_configs

class ConfigurationDescriptor(Descriptor):
    '''Class representing USB configuration descriptor'''

    def __init__(self, data):
        super().__init__(data)
        self._total_descriptor_length = data[2:4]
        self._num_interfaces = data[4]
        self._config_index = data[5]
        self._configuration_descriptor_index = data[6]
        self._power_capability = data[7]
        self._max_power = data[8]
    
    @property
    def wTotalLength(self):
        '''Size of all descriptors in this configuration (bytes)'''
        return self._total_descriptor_length
    
    @property
    def bNumInterfaces(self):
        '''Number of interfaces in this configuration'''
        return self._num_interface
    
    @property
    def bConfigurationValue(self):
        '''Index of this configuration'''
        return self._config_index
    
    @property
    def iConfiguration(self):
        '''Index of string descriptor for this interface'''
        return self._configuration_descriptor_index

    @property
    def bmAttributes(self):
        '''Describes the power capability of this configuration'''
        return self._power_capability
    
    @property
    def bMaxPower(self):
        '''Amount of current drawn when bus-powered'''
        return self._max_power

class InterfaceDescriptor(Descriptor):
    '''Class representing the standard usb interface'''

    def __init__(self, data):
        super().__init__(data)
        self._interface_number = data[2]
        self._alternate_setting = data[3]
        self._num_endpoints = data[4]
        self._interface_class = data[5]
        self._interface_sub_class = data[6]
        self._interface_protocol = data[7]
        self._interface_descriptor_index = data[8]
    
    @property
    def bInterfaceNumber(self):
        '''Index of interface in array of all interfaces supported by this configuration'''
        self._interface_number
    
    @property
    def bAlternateSetting(self):
        '''Value used to select an alternate setting for this interface'''
        return self._alternate_setting
    
    @property
    def bNumEndpoints(self):
        '''Number of endpoints associated with this interface'''
        return self._num_endpoints
    
    @property
    def bInterfaceClass(self):
        '''Class of interface'''
        return self._interface_class
    
    @property
    def bInterfaceSubClass(self):
        '''Sub class of interface'''
        return self._interface_sub_class
    
    @property
    def bInterfaceProtocol(self):
        '''Protocol for communicating with interface'''
        return self._interface_protocol
    
    @property
    def iInterface(self):
        '''Index of string descriptor for this interface'''
        return self._interface_descriptor_index

class InterfaceAssociationDescriptor(Descriptor):
    '''Class representing the interface association descriptor for a given interface'''

    def __init__(self, data):
        super().__init__(data)
        self._first_interface = data[2]
        self._interface_count = data[3]
        self._function_class = data[4]
        self._function_sub_class = data[5]
        self._function_protocol = data[6]
        self._function_descriptor_index = data[7]
    
    @property
    def bFirstInterface(self):
        '''Index of first interface in this interface association'''
        return self._first_interface
    
    @property
    def bInterfaceCount(self):
        '''Number of interfaces in this interface association'''
        return self._interface_count
    
    @property
    def bFunctionClass(self):
        '''Function class for this interface association'''
        return self._function_class
    
    @property
    def bFunctionSubClass(self):
        '''Function sub class for this interface association'''
        return self._function_sub_class
    
    @property
    def bFunctionProtocol(self):
        '''Protocol version of interface association'''
        return self._function_protocol

    @property
    def iFunction(self):
        '''Index for string descriptor for this interface association'''
        return self._function_descriptor_index
