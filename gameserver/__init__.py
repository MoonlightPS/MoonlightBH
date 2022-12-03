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
    
    def __init__(self, game_server: GameServer, sock: socket.socket) -> None:
        self.sock = sock
        self.game_server = game_server

    def handle(self, data: bytes):
        packet = Packet()
        packet.parse(data)

        logger.opt(colors=True).debug(f'<yellow>Socket</yellow> Receive: <cyan>{packet.body}</cyan>')
        if handler := self.game_server.router.get(packet.cmdid):
            handler(self, packet.body)

    def send(self, msg: betterproto.Message, is_after_login: bool = True):
        packet = bytes(Packet(body=msg,is_after_login=is_after_login))
        logger.opt(colors=True).debug(f'<yellow>Socket</yellow> Send: <cyan>{msg}</cyan>')
        self.sock.send(bytes(packet))
        
        

        
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
        self.host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host.bind((host,port))
        print(f'[TCP] Listening on {host}:{port}')
        self.host.listen(1)

    def add(self, router: HandlerRouter):
        self.router.add(router)

    def loop(self) -> None:
        while True:
            try:
                clientsocket,address = self.host.accept()
                self.conns[address] = Connection(self, clientsocket)
                print(f"New connection from {address[1]}.")
                if clientsocket is not None:
                    msg = clientsocket.recv(4096)
                    print("Message received!")
                    conn = self.conns[address]
                    conn.handle(msg)
            except:
                traceback.print_exc()

    def start(self):
        b = threading.Thread(name='GameServer', target=self.loop)
        b.daemon=True
        b.start()