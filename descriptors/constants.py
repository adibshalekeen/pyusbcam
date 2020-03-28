#-------------------------------------#
# Standard USB Descriptors #
#-------------------------------------#
# Device Descriptor
# Describes vid/pid/manufacturer and number of configurations
DT_DEVICE = 0x01

# Configuration Descriptor
# Describes length of descriptors in configuration, number of interfaces and power settings
DT_CONFIG = 0x02

# Interface Association Descriptor
# Describes the video interface collection
DT_IAD = 0x0B

# Video class descriptor type interface
DT_VC_IAD = 0x24

#-------------------------------------#
# Video Control Interface Descriptors #
#-------------------------------------#
# Describes a collection of interfaces making up the video control interface
VC_DESCRIPTOR_UNDEFINED = 0x00
VC_HEADER = 0x01
VC_INPUT_TERMINAL = 0x02
VC_OUTPUT_TERMINAL = 0x03
VC_SELECTOR_UNIT = 0x04
VC_PROCESSING_UNIT = 0x05
VC_EXTENSION_UNIT = 0x06
VC_ENCODING_UNIT = 0x07

#--------------------------------------#
# Video Streaming Interface Descriptor #
#--------------------------------------#
# Describes a collection of interfaces and additional data for video stream control
VS_UNDEFINED = 0x00
VS_INPUT_HEADER = 0x01
VS_OUTPUT_HEADER = 0x02
VS_STILL_IMAGE_FRAME = 0x03
VS_FORMAT_UNCOMPROSSED = 0x04
VS_FRAME_UNCOMPRESSED = 0x05
VS_FORMAT_MJPEG = 0x06
VS_FRAME_MJPEG = 0x07
VS_FORMAT_MPEG2TS = 0x0A
VS_FORMAT_DV = 0x0C
VS_COLORFORMAT = 0x0D
VS_FORMAT_FRAME_BASED = 0x10
VS_FRAME_FRAME_BASED = 0x11
VS_FORMAT_STREAM_BASED = 0x12
VS_FORMAT_H264 = 0x13
VS_FRAME_H264 = 0x14
VS_FORMAT_H264_SIMULCAST = 0x15
VS_FORMAT_VP8 = 0x16
VS_FRAME_VP8 = 0x17
VS_FORMAT_VP8_SIMULCAST = 0x18