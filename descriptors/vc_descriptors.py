import enum
from .usb_descriptors import Descriptor

'''Module containing classes representing usb class-specific video control interface descriptors'''

class VideoControlInterfaceDescriptor(Descriptor):
    '''Class representing a component in the video control interface descriptor'''

    def __init__(self, data):
        super().__init__(data)
        self._sub_type = data[2]
    
    @property
    def bDescriptorSubType(self):
        return self._sub_type

class VCInterfaceHeaderDescriptor(VideoControlInterfaceDescriptor):
    '''Class representing header descriptor for class-specific video control interface'''

    def __init__(self, data):
        super().__init__(data)
        self._uvc_spec = data[3:5]
        self._total_length = data[5:7]
        self._clock_freq = data[7:11]
        self._num_streaming_interfaces = data[11]
        self._streaming_interface_index = data[12:]
    
    @property
    def bcdUVC(self):
        '''UVC protocol specifications for this device'''
        return self._uvc_spec
    
    @property
    def wTotalLength(self):
        '''Total length of all of the descriptors in this video control interface'''
        return self._total_length
    
    @property
    def dwClockFrequency(self):
        '''The device clock frequency'''
        return self._clock_freq
    
    @property
    def bInCollection(self):
        '''Number of video streaming interfaces in this collection'''
        return self._num_streaming_interfaces
    
    @property
    def bInterfaceNr(self):
        '''Array of all the interface indices that are video streaming interfaces'''
        return self._streaming_interface_index

class VCTerminalDescriptor(VideoControlInterfaceDescriptor):
    '''Class representing a terminal descriptor in the video-control interface'''

    def __init__(self, data):
        super().__init__(data)
        self._terminal_id = data[3]
        self._terminal_type = data[4:6]
        self._associated_terminal = data[6]

    @property
    def bTerminalID(self):
        '''Unique identifier used to address this terminal during control requests'''
        return self._terminal_id
    
    @property
    def bTerminalType(self):
        '''Constant characterizing the type of terminal this is'''
        return self._terminal_type
    
    @property
    def bAssocTerminal(self):
        '''Terminal associated with this terminal (zero if none)'''
        return self._output_terminal

class InputTerminalDescriptor(VCTerminalDescriptor):
    '''Class representing the the descriptor for a given input terminal to the device'''

    # Length of the descriptor with no optional fields in bytes
    BASE_LEN = 8

    def __init__(self, data):
        super().__init__(data)
        self._terminal_descriptor_index = data[7]
    
    @property
    def iTerminal(self):
        '''Index of string descriptor describing this terminal'''
        return self._terminal_descriptor_index

class OutputTerminalDescriptor(VCTerminalDescriptor):
    '''Class representing an output terminal descriptor'''

    # Length of the descriptor with no optional fields in bytes
    BASE_LEN = 9

    def __init__(self, data):
        super().__init__(data)
        self._source_id = data[7]
        self._terminal_descriptor_index = data[8]
    
    @property
    def bSourceID(self):
        '''The ID of the unit or input terminal associated with this output terminal'''
        return self._source_id
    
    @property
    def iTerminal(self):
        '''Index of string descriptor describing this terminal'''
        return self._terminal_descriptor_index

class CameraTerminalDescriptor(InputTerminalDescriptor):
    '''Class representing terminal descriptor for the camera'''

    class CameraControls(enum.IntEnum):
        SCANNING_MODE = 0
        AUTO_EXPOSURE_MODE = 1
        AUTO_EXPOSURE_PRIORITY = 2
        EXPOSURE_TIME_ABSOLUTE = 3
        EXPOSURE_TIME_RELATIVE = 4
        FOCUS_ABSOLUTE = 5
        FOCUS_RELATIVE = 6
        IRIS_ABSOLUTE = 7
        IRIS_RELATIVE = 8
        ZOOM_ABSOLUTE = 9
        ZOOM_RELATIVE = 10
        PAN_TILT_ABSOLUTE = 11
        PAN_TILT_RELATIVE = 12
        ROLL_ABSOLUTE = 13
        ROLL_RELATIVE = 14
        FOCUS_AUTO = 17
        PRIVACY = 18
        FOCUS_SIMPLE = 19
        WINDOW = 20
        REGION_OF_INTEREST = 21

    def __init__(self, data):
        super().__init__(data)
        self._obj_focal_length_min = data[8:10]
        self._obj_focal_length_max = data[10:12]
        self._ocular_focal_length = data[12:14]
        self._control_size = data[14]
        self._controls = data[15: 15 + int(self._control_size)]
    
    def check_control_supported(self, control_id):
        '''Check if camera control is supported'''
        return bool((self._controls >> control_id) & 0x01)
    
    @property
    def wObjectiveFocalLengthMin(self):
        '''Value of the minimum focal length if optical zoom is supported (0 otherwise)'''
        return self._obj_focal_length_min
    
    @property
    def wObjectiveFocalLengthMax(self):
        '''Value of the maximum focal length if optical zoom is supported (0 otherwise)'''
        return self._obj_focal_length_max
    
    @property
    def wOcularFocalLength(self):
        '''Value of focal length with no zoom if optical zoom is supported (0 otherwise)'''
        return self._ocular_focal_length
    
    @property
    def bControlSize(self):
        '''Size of available camera controls bitmap'''
        return self._control_size
    
    @property
    def bmControls(self):
        '''Bitmap defining that controls are available via the camera terminal'''
        return self._controls