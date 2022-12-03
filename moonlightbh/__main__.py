from gameserver import GameServer;
from gameserver.handlers import auth
from dispatch.app import run_http_server

if __name__ == "__main__":
    gameserver = GameServer("127.0.0.1", 7070)
    gameserver.add(auth.router)

    gameserver.start()
    run_http_server('0.0.0.0')