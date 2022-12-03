
from __future__ import annotations
from gameserver.protocol.reader import BinaryReader
from gameserver.protocol.cmd_id import CmdId
from lib import proto
import betterproto
import json

PACKET_MAGIC = (0x01234567, 0x89abcdef)

class Packet:
    _packetVersion = 1
    _clientVersion = 0
    _time = 0
    _userId = 0
    _userIp = 0
    _userSessionId = 0
    _CmdId = 0 # Used to be gatewayIp
    _unk = 0 # Used to be CmdId
    _bodyLen = 0


    def __init__(self, body: betterproto.Message = None, is_after_login: bool = True):
        self.has_header = is_after_login
        if self.has_header:
            self.head = bytearray.fromhex("0885a35e10acbf94a00d")

        self.body = body
        if not body == None:
            self.cmdid = CmdId[body.__class__.__name__]

    def parse(self, data: bytes) -> Packet:
        buf = BinaryReader(data)

        self.magic1 = buf.read_u32b()
        if self.magic1 != PACKET_MAGIC[0]:
            raise Exception(f'MAGIC_START does not match')
    
        self._packetVersion = buf.read_u16b()
        self._clientVersion = buf.read_u16b()
        self._time = buf.read_u32b()
        self._userId = buf.read_u32b()
        self._userIp = buf.read_u32b()
        self._userSessionId = buf.read_u32b()
        self._CmdId = buf.read_u32b()
        self._unk = buf.read_u16b()
        self._bodyLen = buf.read_u32b()

        self.cmdid = CmdId(self._CmdId)
        data_len = self._bodyLen

        proto_class = getattr(proto, self.cmdid.name, None)

        if data_len:
            self.body = proto_class().parse(buf.read(data_len))
        else:
            self.body = proto_class()

        # print(json.dumps(json.loads(self.body.to_json()),indent=2))

        self.magic2 = buf.read_u32b()
        if self.magic2 != PACKET_MAGIC[1]:
            raise Exception(f'MAGIC_END does not match')

        return self

    def __bytes__(self) -> bytes:
        if self.body == None:
            raise Exception('Empty Body??? wtf?')

        buf = BinaryReader()

        buf.write_u32b(PACKET_MAGIC[0])
        buf.write_u16b(self._packetVersion)
        buf.write_u16b(self._clientVersion)
        buf.write_u32b(self._time)
        buf.write_u32b(self._userId)
        buf.write_u32b(self._userIp)
        buf.write_u32b(self._userSessionId)
        buf.write_u32b(self._CmdId)
        buf.write_u16b(self._unk)
        buf.write_u32b(self._bodyLen)

        body = bytes(self.body)
        
        if self.has_header:
            buf.write(self.head)

        if len(body) > 0:
            buf.write(body)

        buf.write_u32b(PACKET_MAGIC[1])

        

        return buf.getvalue()