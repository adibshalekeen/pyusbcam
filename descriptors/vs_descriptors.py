'''This module contains classes modeling descriptors for the video-streaming interface'''
import enum
from usb_descriptors import Descriptor


class VideoStreamingInterfaceDescriptor(Descriptor):
    '''Class representing a component in the video streaming interface descriptor'''
    
    def __init__(self, data):
        super().__init__(data)
        self._descriptor_sub_type = data[2]
    
    @property
    def bDescriptorSubType(self):
        '''Subtype of the descriptor'''
        return self._descriptor_sub_type


class VSHeaderDescriptor(VideoStreamingInterfaceDescriptor):
    '''Class representing a video streaming interface input header component'''

    class FrameControls(enum.IntEnum):

        KEY_FRAME_RATE = 0
        PFRAME_RATE = 1
        COMP_QUALITY = 2
        COMP_WINDOW_SIZE = 3
        GENERATE_KEY_FRAME = 4
        UPDATE_FRAME_SEGMENT = 5

    def __init__(self, data):
        super().__init__(data)
        self._num_formats = data[3]
        self._total_length = data[4:6]
        self._endpoint_addr = data[6]
        self._info = data[7]
        self._terminal_link = data[8]
        self._still_capture_method = data[9]
        self._trigger_support = data[10]
        self._trigger_usage = data[11]
        self._control_size = data[12]
        self._controls = []
        for format_index in range(len(self._num_formats)):
            self._controls.append(data[13 + format_index * len(self._control_size) : 13 + (format_index + 1) * len(self._control_size)])

    def check_control_supported(self, control_id, frame_format):
        '''Check if control is supported by this encoder unit'''
        controls = self._controls[frame_format]
        cmd_int = 0
        for byte_index in range(self._control_size):
            cmd_int |= controls[byte_index] << (8 * byte_index)
        return bool((cmd_int >> control_id) & 0x01)

    @property
    def bNumFormats(self):
        '''The number of video formats supported by this video streaming interface'''
        return self._num_formats
    
    @property
    def wTotalLength(self):
        '''The total length of this descriptor in bytes'''
        return self._total_length
    
    @property
    def bEndpointAddress(self):
        '''Address of the isochronous or bulk endpoint used for video data'''
        return self._endpoint_addr
    
    @property
    def bmInfo(self):
        '''Bitmap indicating the capabilities of this video streaming interface'''
        return self._info
    
    @property
    def bTerminalLink(self):
        '''The terminal ID of the output terminal that the video endpoint of the video streaming interface is connected to'''
        return self._terminal_link
    
    @property
    def bStillCaptureMethod(self):
        '''Method of still image capture supported'''
        return self._still_capture_method
    
    @property
    def bTriggerSupport(self):
        '''Whether hardware triggering is supported'''
        return self._trigger_support
    
    @property
    def bTriggerUsage(self):
        '''Specifies how host software will respond to a hardware trigger interrupt event from this video streaming interface'''
        return self._trigger_usage
    
    @property
    def bControlSize(self):
        '''Size of the bitmal defining video interface controls'''
    
    @property
    def bmaControls(self):
        '''Controls for each type of frame format supported'''
        return self._controls

class UncompressedVideoFormatDescriptor(VideoStreamingInterfaceDescriptor):
    '''Class representing uncompressed video format descriptor'''

    def __init__(self, data):
        self._format_index = data[3]
        self._num_frame_descriptors = data[4]
        self._format_guid = data[5:21]
        self._bits_per_pixel = data[21]
        self._default_frame_index = data[22]
        self._aspect_ratio_x = data[23]
        self._aspect_ratio_y = data[24]
        self._interlace_flags = data[25]
        self._copy_protect = data[26]
    
    @property
    def bFormatIndex(self):
        '''Index of this format descriptor'''
        return self._format_index
    
    @property
    def bNumFrameDescriptors(self):
        '''Number of frame descriptors that follow this one associated with this format'''
        return self._num_frame_descriptors
    
    @property
    def guidFormat(self):
        '''Globally unique identifier used to identify stream-encoding format'''
        return self._format_guid
    
    @property
    def bBitsPerPixel(self):
        '''Number of bits per pixel used to specify color in the decoded video frame'''
        return self._bits_per_pixel
    
    @property
    def bDefaultFrameIndex(self):
        '''Optimum frame index for this stream (used to select resolution)'''
        return self._default_frame_index
    
    @property
    def bAspectRatioX(self):
        '''The X dimension of the picture aspect ratio'''
        return self._aspect_ratio_x
    
    @property
    def bAspectRatioY(self):
        '''The Y diemsion of the picture aspect ratio'''
        return self._aspect_ratio_y
    
    @property
    def bmInterlaceFlags(self):
        '''Specifies interlace information for this format'''
        return self._interlace_flags
    
    @property
    def bCopyProtect(self):
        '''Whether duplication of the video stream is restricted'''
        return self._copy_protect

class MJPEGVideoFormatDescriptor(VideoStreamingInterfaceDescriptor):
    '''Class representing MJPEG video format descriptor'''

    def __init__(self, data):
        self._format_index = data[3]
        self._num_frame_descriptors = data[4]
        self._flags = data[5]
        self._default_frame_index = data[6]
        self._aspect_ratio_x = data[7]
        self._aspect_ratio_y = data[8]
        self._interlace_flags = data[9]
        self._copy_protect = data[10]
    
    @property
    def bFormatIndex(self):
        '''Index of this format descriptor'''
        return self._format_index
    
    @property
    def bNumFrameDescriptors(self):
        '''Number of frame descriptors that follow this one associated with this format'''
        return self._num_frame_descriptors
    
    @property
    def bDefaultFrameIndex(self):
        '''Optimum frame index for this stream (used to select resolution)'''
        return self._default_frame_index
    
    @property
    def bAspectRatioX(self):
        '''The X dimension of the picture aspect ratio'''
        return self._aspect_ratio_x
    
    @property
    def bAspectRatioY(self):
        '''The Y diemsion of the picture aspect ratio'''
        return self._aspect_ratio_y
    
    @property
    def bmInterlaceFlags(self):
        '''Specifies interlace information for this format'''
        return self._interlace_flags
    
    @property
    def bCopyProtect(self):
        '''Whether duplication of the video stream is restricted'''
        return self._copy_protect


class VideoFrameDescriptor(VideoStreamingInterfaceDescriptor):
    '''Class representing uncompressed video frame descriptor'''

    def __init__(self, data):
        self._frame_index = data[3]
        self._capabilities = data[4]
        self._width = data[5:7]
        self._height = data[7:9]
        self._min_bit_rate = data[9:13]
        self._max_bit_rate = data[13:17]
        self._max_video_frame_buff_size = data[21:25]
        self._default_frame_interval = data[21:25]
        self._frame_interval_type = data[25]
        self._min_frame_interval = None
        self._max_frame_interval = None
        self._frame_interval_step = None
        self._frame_interval = None
        if self._frame_interval_type == 0:
            self._min_frame_interval = data[26]
            self._max_frame_interval = data[27]
            self._frame_interval_step = data[28]
        else:
            self._frame_interval = []
            for interval_index in range(int(self._frame_interval_type)):
                self._frame_interval.append(data[26 + (interval_index * 4) : 26 + ((interval_index + 1) * 4)])
        
    @property
    def bFrameIndex(self):
        '''Index of frame descriptor in array of frame descriptors of the same format'''
        return self._frame_index
    
    @property
    def bmCapabilities(self):
        '''Capabilities of this frame type'''
        return self._capabilities
    
    @property
    def wWidth(self):
        '''Width of the decoded bitmap frame in pixels'''
        return self._width
    
    @property
    def wHeight(self):
        '''Height of the decoded bitmap frame in pixels'''
        return self._height
    
    @property
    def dwMinBitRate(self):
        '''Specifies the minimum bit rate at the longest frame interval in bits per second at which data can be transmitted'''
        return self._min_bit_rate
    
    @property
    def dwMaxBitRate(self):
        '''Specifies the maxmimum bit rate at the longest frame interval in bits per second at which data can be transmitted'''
        return self._max_bit_rate

    @property
    def dwMaxVideoFrameBufferSize(self):
        '''Maximum number of bytes the compressor will produce for a video frame or still image'''
        return self._max_video_frame_buff_size
    
    @property
    def dwDefaultFrameInterval(self):
        '''Specifies the frame interval the device would like to indicate for use as a default'''
        return self._default_frame_interval
    
    @property
    def bFrameIntervalType(self):
        '''Defines the type of the frame interval setting 0 for continuous, else describes the number of discrete frame intervals'''
        return self._frame_interval_type
    
    @property
    def dwMinFrameInterval(self):
        '''The minimum frame interval supported'''
        return self._min_frame_interval

    @property
    def dwMaxFrameInterval(self):
        '''The maximum frame interval supported'''
        return self._max_frame_interval
    
    @property
    def dwFrameIntervalStep(self):
        '''The granularity of frame interval supported'''
        return self._frame_itnerval_step
    
    @property
    def dwFrameInterval(self):
        '''Frame interval at a given frame interval index'''
        return self._frame_interval