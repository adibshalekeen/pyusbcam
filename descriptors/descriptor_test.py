import pickle
from descriptor_constants import *
from usb_descriptors import *
from vc_descriptors import *
from vs_descriptors import *

descriptor_bytes = pickle.load(open('config_desc', 'rb'))

data_len = len(descriptor_bytes)

class Placeholder:
    curr_interface_type = None
    def __init__(self):
        pass

VC_DESCRIPTOR_CONSTRUCTORS = {
    VC_HEADER: VCInterfaceHeaderDescriptor,
    VC_INPUT_TERMINAL: VCInputTerminalDescriptor,
    VC_OUTPUT_TERMINAL: VCOutputTerminalDescriptor,
    VC_SELECTOR_UNIT: SelectorUnitDescriptor,
    VC_PROCESSING_UNIT: ProcessingUnitDescriptor,
    VC_EXTENSION_UNIT: ExtensionUnitDescriptor,
    VC_ENCODING_UNIT: EncodingUnitDescriptor
}

VS_DESCRIPTOR_CONSTRUCTORS = {
    VS_INPUT_HEADER: VSHeaderDescriptor,
    VS_FORMAT_UNCOMPRESSED: UncompressedVideoFormatDescriptor,
    VS_FORMAT_MJPEG: MJPEGVideoFormatDescriptor,
    VS_FRAME_UNCOMPRESSED: VideoFrameDescriptor,
    VS_FRAME_MJPEG: VideoFrameDescriptor,
    VS_COLORFORMAT: VSColorMatchingDescriptor
}

TYPE_SPECIFIC_INTERFACE_PARSERS = {
    SC_VIDEOCONTROL: VC_DESCRIPTOR_CONSTRUCTORS,
    SC_VIDEOSTREAMING: VS_DESCRIPTOR_CONSTRUCTORS
}

def ClassSpecificInterfaceDescriptorParser(data):
    try:
        return TYPE_SPECIFIC_INTERFACE_PARSERS[Placeholder.curr_interface_type][data[2]](data)
    except KeyError:
        return str(data)

def ClassSpecificEndpointParser(data):
    return "Class Specific Endpoint"

def InterfaceParser(data):
    intf_descriptor = InterfaceDescriptor(data)
    Placeholder.curr_interface_type = intf_descriptor.bInterfaceSubClass


USB_ESCRIPTOR_CONSTRUCTORS = {
    DT_CONFIG: ConfigurationDescriptor,
    DT_ID: InterfaceParser,
    DT_ED: EndpointDescriptor,
    DT_IAD: InterfaceAssociationDescriptor,
    DT_VC_IAD: InterfaceAssociationDescriptor,
    CS_INTERFACE: ClassSpecificInterfaceDescriptorParser,
    CS_ENDPOINT: ClassSpecificEndpointParser
}

while data_len > 0:
    descriptor_len = int(descriptor_bytes[0])
    descriptor = descriptor_bytes[0:descriptor_len]
    descriptor_bytes = descriptor_bytes[descriptor_len:]
    data_len -= descriptor_len
    try:
        print(USB_ESCRIPTOR_CONSTRUCTORS[descriptor[1]](descriptor))
    except KeyError:
        print("wtf")