from gameserver.protocol.packet import Packet
from gameserver.protocol.cmd_id import CmdId
from gameserver import HandlerRouter,Connection
from lib.proto import AccountType, CgType, GetPlayerTokenReq,GetPlayerTokenRsp,PlayerLoginReq,PlayerLoginRsp,GetPlayerTokenRspRetcode,UserType,PlayerLoginRspRetcode
router = HandlerRouter()

@router(CmdId.GetPlayerTokenReq)
def handle_token_req(conn: Connection, msg: GetPlayerTokenReq):
    rsp = GetPlayerTokenRsp(
        retcode= GetPlayerTokenRspRetcode.SUCC,
        uid=1,
        is_bind_access=False,
        account_uid="1",
        hoyolab_account_uid="1",
        account_type=AccountType.ACCOUNT_HOYOLAB,
        user_type=UserType.USER_TYPE_CHANNEL
    )
    conn.send(rsp,False)

@router(CmdId.PlayerLoginReq)
def handle_login(conn: Connection, msg: PlayerLoginReq):
    rsp = PlayerLoginRsp(
        retcode=PlayerLoginRspRetcode.SUCC,
        cg_type=CgType.CG_SEVEN_CHAPTER,
        region_id=246,
        region_name="MoonlightBH",
        is_first_login=True,
        login_session_token=50647798
    )
    conn.send(rsp,False)