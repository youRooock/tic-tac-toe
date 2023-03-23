import uuid
from mark import Mark

class Player:
    def __init__(self, id: int, mark: Mark):
        self.id = id
        self.mark = mark