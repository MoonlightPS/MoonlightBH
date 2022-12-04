from gameserver.protocol.packet import Packet
from gameserver.protocol.cmd_id import CmdId
from gameserver import HandlerRouter,Connection
from lib.proto import GetPlayerTokenReq,GetPlayerTokenRsp,PlayerLoginReq,PlayerLoginRsp,GetPlayerTokenRspRetcode

router = HandlerRouter()

@router(CmdId.GetPlayerTokenReq)
def handle_token_req(conn: Connection, msg: GetPlayerTokenReq):
    rsp = GetPlayerTokenRsp(
        retcode= GetPlayerTokenRspRetcode.SUCC,
        uid=1,
        account_type=24,
        user_type=4,
        account_uid="1",
        hoyolab_account_uid="1",
        token=msg.token,
    )
    conn.send(rsp,False)

@router(CmdId.PlayerLoginReq)
def handle_login(conn: Connection, msg: PlayerLoginReq):
    rsp = PlayerLoginRsp()
    conn.send(rsp,False)