import grpc
import time
from threading import Thread
from typing import Tuple, List, Dict
from concurrent import futures
from server import Server
from election_service import ElectionService
from game_service import GameService
from command_handlers.list_board_command_handler import Handler
from command_handlers.list_board_command_handler import ListBoardCommandHandler
from command_handlers.set_symbol_command_handler import SetSymbolCommandHandler
from command_handlers.start_game_command_handler import StartGameCommandHandler

def parse_command_and_args(command: str) -> Tuple[str, List[str]]:
    arguments = command.split(' ')

    return (arguments[0], arguments[1:])

if __name__ == "__main__":
    print('Select node_id [0,1,2]')
    server_id = int(input('> '))
    game_service = GameService(server_id)
    election_service = ElectionService(server_id, game_service.start_game)
    handlers: Dict[str, Handler] = {
        'start-game': StartGameCommandHandler(election_service),
        'list-board': ListBoardCommandHandler(),
        'set-symbol': SetSymbolCommandHandler(),
    }

    # we need a new thread in order not to block handling commands
    Thread(target=Server(server_id, election_service, game_service).start).start()

    time.sleep(1)

    print('The app is up and ready to serve commands')
    print('Available commands:')
    print('\tstart-game')
    print('\tset-symbol [position] [O | X]')
    print('\tlist-board')

    while True:
        command, args = parse_command_and_args(input('> '))

        if command not in handlers:
            print(f'Not supported command')
            continue

        handlers[command].handle(args + [server_id])
    

