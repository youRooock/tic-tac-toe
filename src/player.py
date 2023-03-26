import uuid

from mark import Mark


class Player:
    def __init__(self, id: int, mark: Mark):
        self.id = id
        self.mark = mark

    def __eq__(self, o):
        return isinstance(o, Player) and self.id == o.id and self.mark == o.mark
