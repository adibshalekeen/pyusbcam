'''This module contains classes representing standard USB descriptors'''
class Descriptor:
    def __init__(self, data):
        self._length = data[0]
        self._descriptor_type = data[1]

    @property
    def length(self):
        '''The length of the descriptor'''
        return self._length
    
    @property
    def descriptor_type (self):
        '''The type code of the descriptor'''
        return self._descriptor_type

class DeviceDescriptor(Descriptor):
    '''Class representing USB device descriptors'''

    def __init__(self, data):
        super().__init__(data)
        self._usb_version = data[2:4]
        self._device_class = data[4]
        self._device_sub_class = data[5]
        self._max_packet_size = data[6]
        self._vid = data[7:9]
        self._pid = data[9:11]
        self._device_release_code = data[11:13]
        self._mid_str_index = data[13]
        self._product_name_index = data[14]
        self._serial_number = data[15]
        self._num_configs = data[16]
    
    @property
    def usb_version(self):
        '''USB Specification version'''
        self._usb_version
    
    @property
    def device_class(self):
        '''Class ID of the device'''
        return self._device_class
    
    @property
    def device_sub_class(self):
        '''Sub class ID of the device'''
        return self._device_sub_class
    
    @property
    def max_packet_size(self):
        '''Maximum packet size of the control interface'''
        return self._max_packet_size
    
    @property
    def vendor_id(self):
        '''Vendor ID of the device'''
        return self._vid
    
    @property
    def product_id(self):
        '''Product ID of the device'''
        return self._pid
    
    @property
    def device_release_code(self):
        '''Product version of the device (Manufacturer controlled)'''
        return self._device_release_code
    
    @property
    def manufacturer_id_index(self):
        '''Index of the manufacturer ID string descriptor'''
        return self._mid_str_index
    
    @property
    def product_name_index(self):
        '''Index of the product name string descriptor'''
        return self._product_name_index
    
    @property
    def num_configs(self):
        '''The number of configurations this device supports'''
        return self._num_configs

class ConfigurationDescriptor(Descriptor):
    '''Class describing USB configuration descriptor'''

    def __init__(self, data):
        super().__init__(data)
        self._total_descriptor_length = data[2:4]
        self._num_interfaces = data[4]
        self._config_index = data[5]
        self._power_capability = data[6]
        self._max_power = data[7]
    
    @property
    def total_descriptor_length(self):
        '''Size of all descriptors in this configuration (bytes)'''
        return self._total_descriptor_length
    
    @property
    def num_interfaces(self):
        '''Number of interfaces in this configuration'''
        return self._num_interface
    
    @property
    def config_index(self):
        '''Index of this configuration'''
        return self._config_index
    
    @property
    def power_capability(self):
        '''Describes the power capability of this configuration'''
        return self._power_capability
    
    @property
    def max_power(self):
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
    def interface_number(self):
        '''Index of interface in array of all interfaces supported by this configuration'''
        self._interface_number
    
    @property
    def alternate_setting(self):
        '''Value used to select an alternate setting for this interface'''
        return self._alternate_setting
    
    @property
    def num_endpoints(self):
        '''Number of endpoints associated with this interface'''
        return self._num_endpoints
    
    @property
    def interface_class(self):
        '''Class of interface'''
        return self._interface_class
    
    @property
    def interface_sub_class(self):
        '''Sub class of interface'''
        return self._interface_sub_class
    
    @property
    def interface_protocol(self):
        '''Protocol for communicating with interface'''
        return self._interface_protocol
    
    @property
    def interface_descriptor_index(self):
        '''Index of string descriptor for this interface'''
        return self._interface_descriptor_index

class InterfaceAssociationDescriptor(Descriptor):
    '''Class describing the interface association descriptor for a given configuration'''

    def __init__(self, data):
        super().__init__(data)
        self._first_interface = data[2]
        self._interface_count = data[3]
        self._function_class = data[4]
        self._function_sub_class = data[5]
        self._function_descriptor_index = data[7]
    
    @property
    def first_interface(self):
        '''Control interface for the set of interfaces described by this association descriptor'''
        return self._first_interface
    
    @property
    def interface_count(self):
        '''Number of interfaces that are associated with this descriptor'''
        return self._interface_count
    
    @property
    def function_class(self):
        '''Function class for this interface association'''
        return self._function_class
    
    @property
    def function_sub_class(self):
        '''Function sub class for this interface association'''
        return self._function_sub_class
    
    @property
    def function_descriptor_index(self):
        '''Index for string descriptor for this interface association'''
        return self._function_descriptor_index
