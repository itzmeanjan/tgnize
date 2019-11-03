#!/usr/bin/python3

from __future__ import annotations
from typing import List
from user import User


class Chat:
    def __init__(self, users: List[User]):
        self.users = users


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
