from __future__ import annotations
import threading
import socketserver
import socket
from gameserver.protocol.packet import Packet
from gameserver.protocol.cmd_id import CmdId
from typing import Callable
import betterproto
from loguru import logger
import sys

class Connection(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            self.data = self.request.recv(2048).strip()
            packet = Packet().parse(self.data)
            if handler := self.server.router.get(packet.cmdid):
                logger.opt(colors=True).debug(f'<yellow>{self.client_address[0]}</yellow> Receive: <cyan>{packet.body}</cyan>')
                handler(self, packet.body)
            else:
                logger.opt(colors=True).warning(f'<red>Unhandled Packet:</red> <cyan>{packet.body}</cyan>')

    def send(self, msg: betterproto.Message, is_after_login: bool = True):
        packet = Packet(body=msg,is_after_login=is_after_login)
        logger.opt(colors=True).debug(f'<yellow>{self.server.server_address[0]}</yellow> Send: <cyan>{msg}</cyan>')
        self.request.send(bytes(packet))
        

    def close(self):
        logger.opt(colors=True).info(f'<yellow>Closing Connection from</yellow><cyan> {self.client_address[0]}:{self.client_address[1]}</cyan>')
        self.request.close()
        
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


class GameServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    router: HandlerRouter = HandlerRouter()
    conns: dict[str, Connection] = {}

    def __init__(self, host,port):
        socketserver.TCPServer.__init__(self, (host,port), Connection)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
    
    def start_server(self):
        print(f'[TCP] Listening on {self.server_address[0]}:{self.server_address[1]}')
        try:
            self.serve_forever()
        except KeyboardInterrupt:
                sys.exit(0)
        
    def add(self, router: HandlerRouter):
        self.router.add(router)

    def stop(self):
        self.shutdown()
        self.server_close()

    def start(self):
        b = threading.Thread(name='GameServer', target=self.start_server)
        b.daemon=True
        b.start()