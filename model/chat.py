#!/usr/bin/python3

from __future__ import annotations
from typing import List
from user import User


class Chat:
    def __init__(self, users: List[User]):
        self.users = users

    def __getPushPosition__(self, user: User, low: int, high: int) -> int:
        if low > high:
            return 0
        elif low == high:
            return low if self.users[low].name > user.name else (low + 1)
        else:
            mid = (low + high) // 2
            return self.__getPushPosition__(user, low, mid) if self.users[mid].name >= user.name \
                else self.__getPushPosition__(user, mid + 1, high)

    def pushUser(self, user: User):
        self.users.insert(self.__getPushPosition__(
            user, 0, len(self.users) - 1), user)

    def __getUser__(self, user: str, low: int, high: int) -> int:
        if low > high:
            return -1
        elif low == high:
            return low if self.users[low].name == user else -1
        else:
            mid = (low + high) // 2
            return self.__getUser__(user, low, mid) if self.users[mid].name >= user \
                else self.__getUser__(user, mid + 1, high)

    def getUser(self, user: str) -> User:
        idx = self.__getUser__(user, 0, len(self.users) - 1)
        return None if idx == -1 else self.users[idx]


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
