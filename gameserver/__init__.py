from __future__ import annotations
import threading
import socket
from gameserver.protocol.packet import Packet
from gameserver.protocol.cmd_id import CmdId
from typing import Callable
import betterproto
from loguru import logger
import traceback


class Connection:
    game_server: GameServer
    sock: socket.socket
    client_address: socket._Address
    server_address: socket._Address

    def __init__(self, game_server: GameServer, sock: socket.socket, client_address: socket._Address, server_address: socket._Address) -> None:
        self.sock = sock
        self.client_address = client_address
        self.server_address = server_address
        self.game_server = game_server

    def handle(self, data: bytes):
        packet = Packet()
        packet.parse(data)

        logger.opt(colors=True).debug(
            f'<yellow>{self.client_address[0]}</yellow> Receive: <cyan>{packet.body}</cyan>')
        if handler := self.game_server.router.get(packet.cmdid):
            handler(self, packet.body)

    def send(self, msg: betterproto.Message, is_after_login: bool = True):
        packet = bytes(Packet(body=msg, is_after_login=is_after_login))
        logger.opt(colors=True).debug(
            f'<yellow>{self.server_address[0]}</yellow> Send: <cyan>{msg}</cyan>')
        self.send_raw(bytes(packet))

    def send_raw(self,msg: bytes):
        self.sock.sendall(msg)


Handler = Callable[[Connection, Packet], None]


class HandlerRouter:
    _handlers: dict[CmdId, HandlerRouter]

    def __init__(self):
        self._handlers = {}

    def add(self, router: HandlerRouter):
        self._handlers |= router._handlers

    def get(self, cmdid: CmdId) -> Handler | None:
        return self._handlers.get(cmdid)

    def __call__(self, cmdid: CmdId):
        def wrapper(handler: HandlerRouter):
            self._handlers[cmdid] = handler
            return handler
        return wrapper


class GameServer:
    router: HandlerRouter = HandlerRouter()
    conns: dict[str, Connection] = {}

    def __init__(self, host, port) -> None:
        self.host, self.port = host, port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        print(f'[TCP] Listening on {host}:{port}')
        self.server.listen(5)

    def add(self, router: HandlerRouter):
        self.router.add(router)

    def loop(self) -> None:
        while True:
            try:
                clientsocket, address = self.server.accept()
                self.conns[address] = Connection(self, clientsocket, address, (self.host, self.port))
                logger.opt(colors=True).info(f'<cyan>Client connected from </cyan><yellow>{address[0]}:{address[1]}</yellow>')
                while clientsocket is not None:
                    try:
                        msg = clientsocket.recv(2048)
                        conn = self.conns[address]
                        conn.handle(msg)
                    except ConnectionResetError:
                        logger.opt(colors=True).info(f'<yellow>{address[0]}:{address[1]}</yellow> <cyan>has disconnected!</cyan>')
                        break
            except:
                traceback.print_exc()

    def start(self):
        b = threading.Thread(name='GameServer', target=self.loop)
        b.daemon = True
        b.start()
