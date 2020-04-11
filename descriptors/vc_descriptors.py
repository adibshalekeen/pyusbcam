import enum
from usb_descriptors import Descriptor

'''Module containing classes representing usb class-specific video control interface descriptors'''


class VideoControlInterfaceDescriptor(Descriptor):
    '''Class representing a component in the video control interface descriptor'''

    def __init__(self, data):
        super().__init__(data)
        self._sub_type = data[2]
    
    @property
    def bDescriptorSubType(self):
        return self._sub_type


class VideoControlEndpointDescriptor(VideoControlInterfaceDescriptor):
    '''Class representing an endpoint descriptor for a video control interface'''

    def __init__(self, data):
        super().__init__(data)
        self._max_transfer_size = data[3:5]
    
    @property
    def wMaxTransferSize(self):
        '''The maximum packet size for this endpoint'''
        return self._max_transfer_size


class VCInterfaceHeaderDescriptor(VideoControlInterfaceDescriptor):
    '''Class representing header descriptor for a video control interface'''

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


class VCInputTerminalDescriptor(VCTerminalDescriptor):
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


class VCOutputTerminalDescriptor(VCTerminalDescriptor):
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


class CameraTerminalDescriptor(VCInputTerminalDescriptor):
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
        ctrl_int = 0
        for byte_index in range(self._control_size):
            ctrl_int |= (self._controls[byte_index] << (byte_index * 8))
        return bool((ctrl_int >> control_id) & 0x01)
    
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


class VCUnitDescriptor(VideoControlInterfaceDescriptor):
    '''Class representing a video control unit descriptor'''

    def __init__(self, data):
        self._unit_id = data[3]

    @property
    def bUnitID(self):
        '''A non-zero constant that uniquely identifies the unit within the video control interface'''
        return self._unit_id


class SelectorUnitDescriptor(VCUnitDescriptor):
    '''Class representing a selector unit descriptor'''

    def __init__(self, data):
        self._num_input_pins = data[4]
        self._pin_addrs = data[5:5 + int(self._num_input_pins)]
        self._selector_unit_descriptor_index = data[5 + int(self._num_input_pins)]
    
    @property
    def bNrInPins(self):
        '''Number of input pins to this unit'''
        return self._num_input_pins
    
    @property
    def baSourceID(self):
        '''Unique ID of the unit / terminal corresponding to each pin'''
        return self._pin_addrs
    
    @property
    def iSelector(self):
        '''Index of the string descriptor describing this selector unit'''
        return self._selector_unit_descriptor_index


class ProcessingUnitDescriptor(VCUnitDescriptor):
    '''Class representing a processing unit descriptor'''

    class ProcessorControls(enum.IntEnum):
        BRIGHTNESS = 0
        CONTRAST = 1
        HUE = 2
        SATURATION = 3
        SHARPNESS = 4
        GAMMA = 5
        WHITE_BALANCE_TEMP = 6
        WHITE_BALANCE_COMPONENT = 7
        BACKLIGHT_COMPENSATION = 8
        GAIN = 9
        POWER_LINE_FREQUENCY = 10
        HUE_AUTO = 11
        WHITE_BALANCE_TEMPERATURE_AUTO = 12
        WHITE_BALANCE_COMPONENT_AUTO = 13
        DIGITAL_MULTIPLIER = 14
        DIGITAL_MULTIPLIER_LIMIT = 15
        ANALOG_VIDEO_STANDARD = 16
        ANALOG_VIDEO_LOCK_STATUS = 17
        CONTRAST_AUTO = 18

    class ProcessorAnalogVideoStandards(enum.IntEnum):
        NONE = 0
        NTSC = 1
        PAL = 2
        SECAM = 3
        NTSC_2 = 4
        PAL_2 = 5

    def __init__(self, data):
        self._source_id = data[4]
        self._max_multiplier = data[5:7]
        self._control_size = data[7]
        self._controls = data[8:(8 + int(self._control_size))]
        self._processing_unit_descriptor_index = data[8 + int(self._control_size)]
        try:
            self._video_standards = data[8 + int(self._control_size) + 1]
        except IndexError:
            self._video_standards = 0
    
    def check_control_supported(self, control_id):
        '''Check if control id is supported by processing unit'''
        ctrl_int = 0
        for byte_index in range(self._control_size):
            ctrl_int |= (self._controls[byte_index] << (byte_index * 8))
        return bool((ctrl_int >> control_id) & 0x01)

    def check_analog_standard_supported(self, analog_standard_id):
        '''Check if analog standard is supported by processing unit'''
        return bool((self._video_standards >> analog_standard_id) & 0x01)

    @property
    def bSourceID(self):
        '''The source ID of the unit or terminal connected to the input pin of the processing unit'''
        return self._source_id
    
    @property
    def wMaxMultiplier(self):
        '''Indicates maximum digital magnification multiplied by 100 (if control is supported)'''
        return self._max_multiplier
    
    @property
    def bControlSize(self):
        '''The size of the controls bitmap'''
        return self._control_size
    
    @property
    def bmControls(self):
        '''Bitmap describing the supported controls for this processing unit'''
        return self._controls
    
    @property
    def iProcessing(self):
        '''Index of string descriptor describing this processing unit'''
        return self._processing_unit_descriptor_index

    @property
    def bmVideoStandards(self):
        '''Bit map describing all the analog video standards supported by this processing unit'''
        return self._video_standards


class EncodingUnitDescriptor(VCUnitDescriptor):
    '''Class representing encoding unit descriptor'''

    class EncoderControls(enum.IntEnum):
        SELECT_LAYER = 0
        PROFILE_AND_TOOLSET = 1
        VIDEO_RESOLUTION = 2
        MINIMUM_FRAME_INTERVAL = 3
        SLICE_MODE = 4
        RATE_CONTROL_MODE = 5
        AVERAGE_BIT_RATE = 6
        CPB_SIZE = 7
        PEAK_BIT_RATE = 8
        QUANTIZATION_PARAM = 9
        SYNC_AND_LT_REFERENCE_FRAME = 10
        LONG_TERM_BUFFER = 11
        PICTURE_LONG_TERM_REFERENCE = 12
        LTR_VALDIATION = 13
        LEVEL_IDC = 14
        SEI_MESSAGE = 15
        QP_RANGE = 16
        PRIORITY_ID = 17
        START_STOP_LAYER = 18
        ERROR_RESILIENCY = 19

    def __init__(self, data):
        super().__init__(data)
        self._source_id = data[4]
        self._encoding_unit_descriptor_index = data[5]
        self._control_size = data[6]
        self._controls = data[6:6 + int(self._control_size)]
        self._controls_runtime = data[6 + int(self._control_size):6 + (2 * int(self._control_size))]
    
    def check_control_supported(self, control_id):
        '''Check if control is supported by this encoder unit'''
        ctrl_int = 0
        for byte_index in range(self._control_size):
            ctrl_int |= (self._controls[byte_index] << (byte_index * 8))
        return bool((ctrl_int >> control_id) & 0x01)
    
    def check_control_runtime_supported(self, control_id):
        '''Check if control is supported during run time'''
        return bool((self._controls_runtime >> control_id) & 0x01)
    
    @property
    def bSourceID(self):
        '''Id of the unit or terminal connected to the input pin of this encoder unit'''
        return self._source_id
    
    @property
    def iEncoding(self):
        '''Index of the string descriptor describing this encoder unit'''
        return self._encoding_unit_descriptor_index
    
    @property
    def bControlSize(self):
        '''Size of the controls & runtime controls bitmap'''
        return self._control_size
    
    @property
    def bmControls(self):
        '''Bitmap representing set of controls supported by this encoder unit'''
        return self._controls
    
    @property
    def bmControlsRuntime(self):
        '''Bitmap representing set of controls supported by this encoder unit at runtime'''
        return self._controls_runtime


class ExtensionUnitDescriptor(VCUnitDescriptor):
    '''Class representing the extension unit descriptor'''

    def __init__(self, data):
        super().__init__(data)
        self._extension_code = data[4 : 20]
        self._num_controls = data[20]
        self._num_input_pins = data[21]
        self._pin_addrs = data[22:22 + int(self._num_input_pins)]
        self._control_size = data[22 + int(self._num_input_pins)]
        self._controls = data[23 + int(self._num_input_pins): 23 + int(self._num_input_pins) + int(self._control_size)]
        self._extension_unit_descriptor_index = data[23 + int(self._num_input_pins) + int(self._control_size)]
    
    @property
    def guidExtensionCode(self):
        '''Vendor specific code identifying this extension unit'''
        return self._extension_code
    
    @property
    def bNumControls(self):
        '''Number of controls supported by this extension unit'''
        return self._num_controls
    
    @property
    def bNrInPins(self):
        '''Number of input pins to the extension unit'''
        return self._num_input_pins
    
    @property
    def baSourceID(self):
        '''ID of the unit or terminal connected to each input pin of the extension unit'''
        return self._pin_addrs
    
    @property
    def bControlSize(self):
        '''Size of the controls bitmap'''
        return self._control_size
    
    @property
    def bmControls(self):
        '''Bitmap representing the set of controls supported by the extension unit'''
        return self._controls

def VCInterruptEndpointDescriptor(VideoControlInterfaceDescriptor):

    def __init__(self, data):
        super().__init__(data)
        self._max_transfer_size = data[3:5]
    
    @property
    def wMaxTransferSize(self):
        '''Maximum interrupt structure size this endpoint is capable of sending'''
        return self._max_transfer_size