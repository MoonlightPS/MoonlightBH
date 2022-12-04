from gameserver.protocol.packet import Packet
from gameserver.protocol.cmd_id import CmdId
from gameserver import HandlerRouter,Connection
from lib.proto import KeepAliveNotify

router = HandlerRouter()

@router(CmdId.KeepAliveNotify)
def handle_keep_alive(conn: Connection, msg: KeepAliveNotify):
    print('KeepAliveNotify Received!!')
    pass