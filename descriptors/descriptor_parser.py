from .descriptor_constants import *
from .usb_descriptors import *
from .vc_descriptors import *
from .vs_descriptors import *

class DescriptorParser:
    '''Helper class used to parse all configuration descriptors'''

    CLASS_SPECIFIC_CONSTRUCTORS = {
        SC_VIDEOCONTROL: {
            VC_HEADER: VCInterfaceHeaderDescriptor,
            VC_INPUT_TERMINAL: VCInputTerminalDescriptor,
            VC_OUTPUT_TERMINAL: VCOutputTerminalDescriptor,
            VC_SELECTOR_UNIT: SelectorUnitDescriptor,
            VC_PROCESSING_UNIT: ProcessingUnitDescriptor,
            VC_EXTENSION_UNIT: ExtensionUnitDescriptor,
            VC_ENCODING_UNIT: EncodingUnitDescriptor
        },
        SC_VIDEOSTREAMING: {
            VS_INPUT_HEADER: VSHeaderDescriptor,
            VS_FORMAT_UNCOMPRESSED: UncompressedVideoFormatDescriptor,
            VS_FORMAT_MJPEG: MJPEGVideoFormatDescriptor,
            VS_FRAME_UNCOMPRESSED: VideoFrameDescriptor,
            VS_FRAME_MJPEG: VideoFrameDescriptor,
            VS_COLORFORMAT: VSColorMatchingDescriptor
        }
    }

    @classmethod
    def USBInterfaceParser(cls, data):
        intf = InterfaceDescriptor(data)
        DescriptorParser.CURR_INTF_TYPE = intf.bInterfaceSubClass
        return intf
    
    @classmethod
    def ClassSpecificInterfaceParser(cls, data):
        return DescriptorParser.CLASS_SPECIFIC_CONSTRUCTORS[DescriptorParser.CURR_INTF_TYPE][data[2]](data)

    @classmethod
    def ClassSpecificEndpointParser(cls, data):
        return VCInterruptEndpointDescriptor(data)

    def __init__(self, data):
        self._curr_interface_type = None
        self.USB_CONSTRUCTORS = {
            DT_CONFIG: ConfigurationDescriptor,
            DT_ID: DescriptorParser.USBInterfaceParser,
            DT_ED: EndpointDescriptor,
            DT_IAD: InterfaceAssociationDescriptor,
            DT_VC_IAD: InterfaceAssociationDescriptor,
            CS_INTERFACE: DescriptorParser.ClassSpecificInterfaceParser,
            CS_ENDPOINT: DescriptorParser.ClassSpecificEndpointParser
        }

        data_len = len(data)
        while data_len > 0:
            sub_len = int(data[0])
            desc_data = data[0:sub_len]
            data = data[sub_len:]
            data_len -= sub_len
            try:
                print(self.USB_CONSTRUCTORS[desc_data[1]](desc_data))
            except KeyError:
                print(f"Invalid descriptor {desc_data}")
