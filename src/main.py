import grpc
import sys
import os
import threading
import random
import time
import typer
from typing import Tuple, List, Dict
from config import servers
from concurrent import futures
from server import Server
from command_handlers.list_board_command_handler import Handler
from command_handlers.list_board_command_handler import ListBoardCommandHandler
from command_handlers.set_symbol_command_handler import SetSymbolCommandHandler
from command_handlers.start_game_command_handler import StartGameCommandHandler

def run_server(node_id: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # tiny_url_pb2_grpc.add_TinyUrlServiceServicer_to_server(TinyUrlController(), server)
    server.add_insecure_port(f'[::]:{get_leader_port(node_id)}')
    server.start()
    print("server is up and running ...")
    server.wait_for_termination()

def get_leader_port(leader_node_id: int) -> int:
    return f'5000{leader_node_id}'

def parse_command_and_args(command: str) -> Tuple[str, List[str]]:
    arguments = command.split(' ')

    return (arguments[0], arguments[1:])


if __name__ == "__main__":
    print('Select node_id [1,2,3]')
    node_id = int(input('> '))

    handlers: Dict[str, Handler] = {
        'start-game': StartGameCommandHandler(node_id, [server[0] for server in servers], Server()),
        'list-board': ListBoardCommandHandler(),
        'set-symbol': SetSymbolCommandHandler(),
    }

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

        handlers[command].handle(args + [node_id])

