from gameserver import GameServer;
from dispatch.app import run_http_server
from gameserver.handlers import auth, online

if __name__ == "__main__":
    gameserver = GameServer("127.0.0.1", 7070)
    gameserver.add(auth.router)
    gameserver.add(online.router)
    gameserver.start()
    run_http_server('127.0.0.1')