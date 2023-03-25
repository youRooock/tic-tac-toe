from config import available_servers


def find_next(server_id):
    return (server_id + 1) % len(available_servers)
