import uuid
from mark import Mark

class Player:
    def __init__(self, mark: Mark):
        self.id = uuid.uuid1()
        self.mark = mark