#-------------------------------------#
# Standard USB Descriptors #
#-------------------------------------#
# Device Descriptor
# Describes vid/pid/manufacturer and number of configurations
DT_DEVICE = 0x01

# Configuration Descriptor
# Describes length of descriptors in configuration, number of interfaces and power settings
DT_CONFIG = 0x02

# Standard USB interface descriptor
DT_ID = 0x04

# Standard USB endpoint descriptor
DT_ED = 0x05

# Interface Association Descriptor
# Describes the video interface collection
DT_IAD = 0x0B

# Video class descriptor type interface
DT_VC_IAD = 0x24

#-------------------------------------#
# Video Control Interface Descriptors #
#-------------------------------------#
# Describes a collection of interfaces making up the video control interface
# Interface subclass codes
SC_UNDEFINED = 0x00
SC_VIDEOCONTROL = 0x01
SC_VIDEOSTREAMING = 0x02
SC_VIDEO_INTERFACE_COLLECTION = 0x03

CS_UNDEFINED = 0x20
CS_DEVICE = 0x21
CS_CONFIGURATION = 0x22
CS_STRING = 0x23
CS_INTERFACE = 0x24
CS_ENDPOINT = 0x25

VC_DESCRIPTOR_UNDEFINED = 0x00
VC_HEADER = 0x01
VC_INPUT_TERMINAL = 0x02
VC_OUTPUT_TERMINAL = 0x03
VC_SELECTOR_UNIT = 0x04
VC_PROCESSING_UNIT = 0x05
VC_EXTENSION_UNIT = 0x06
VC_ENCODING_UNIT = 0x07

ITT_VENDOR_SPECIFIC = 0x0200
ITT_CAMERA = 0x0201
ITT_MEDIA_TRANSPORT_INPUT = 0x202

OTT_VENDOR_SPECIFIC = 0x0300
OTT_DISPLAY = 0x301
OTT_MEDIA_TRANSPORT_OUTPUT = 0x0302
OTT_STREAMING = 0x0101

#--------------------------------------#
# Video Streaming Interface Descriptor #
#--------------------------------------#
# Describes a collection of interfaces and additional data for video stream control
VS_UNDEFINED = 0x00
VS_INPUT_HEADER = 0x01
VS_OUTPUT_HEADER = 0x02
VS_STILL_IMAGE_FRAME = 0x03
VS_FORMAT_UNCOMPRESSED = 0x04
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