import time
from concurrent import futures
from threading import Thread
from typing import Dict, List, Tuple

import grpc

from clock_service import ClockService
from command_handlers import (
    Handler,
    ListBoardCommandHandler,
    SetNodeTimeCommandHandler,
    SetSymbolCommandHandler,
    StartGameCommandHandler,
)
from election_service import ElectionService
from game_service import GameService
from server import Server


def parse_command_and_args(command: str) -> Tuple[str, List[str]]:
    arguments = command.split(" ")

    return (arguments[0], arguments[1:])


if __name__ == "__main__":
    print("Select node_id [0,1,2]")
    server_id = int(input("> "))

    clock_service = ClockService(server_id)
    game_service = GameService(server_id)
    election_service = ElectionService(server_id)

    clock_service.configure(
        get_leader_id=election_service.get_leader_id,
    )
    game_service.configure(
        get_time_function=clock_service.get_local_time,
        get_game_master_id=election_service.get_leader_id,
    )
    election_service.configure(
        start_game_callback=game_service.initiate,
        sync_clock_callback=clock_service.sync_clock,
    )

    handlers: Dict[str, Handler] = {
        "start-game": StartGameCommandHandler(election_service),
        "list-board": ListBoardCommandHandler(game_service),
        "set-symbol": SetSymbolCommandHandler(game_service),
        "set-node-time": SetNodeTimeCommandHandler(clock_service),
    }

    # we need a new thread in order not to block handling commands
    Thread(target=Server(server_id, election_service, game_service, clock_service).start).start()

    time.sleep(1)

    print("The app is up and ready to serve commands")
    print("Available commands:")
    print("\tstart-game")
    print("\tset-symbol [position]")
    print("\tlist-board")
    print("\tset-node-time [server-id] [hh:mm:ss]")

    while True:
        command, args = parse_command_and_args(input("> "))

        if command not in handlers:
            print(f"Not supported command")
            continue

        handlers[command].handle(args + [server_id])
