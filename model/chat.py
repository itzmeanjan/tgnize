#!/usr/bin/python3

from __future__ import annotations
from typing import List
from activity import Activity


class Chat:

    def __init__(self, activities: List[Activity]):
        self.activities = activities

    def __iter__(self):
        return iter(self.activities)

    def __getPushPosition__(self, idx: int, low: int, high: int):
        if low > high:
            return 0
        elif low == high:
            return low if self.activities[low].index > idx else (low + 1)
        else:
            mid = (low + high) // 2
            return self.__getPushPosition__(idx, low, mid) \
                if self.activities[mid].index > idx \
                else self.__getPushPosition__(idx, mid + 1, high)

    def push(self, item: Activity):
        self.activities.insert(self.__getPushPosition__(
            item.index, 0, len(self.activities) - 1), item)

    def isEvent(self, idx: int) -> bool:
        try:
            self.activities[idx].user
            return False
        except Exception:
            return True

    def __getItem__(self, idx: int, low: int, high: int) -> int:
        if low > high:
            return -1
        elif low == high:
            return low if self.activities[low].index == idx else -1
        else:
            mid = (low + high) // 2
            return self.__getItem__(idx, low, mid) \
                if self.activities[mid].index >= idx \
                else self.__getItem__(idx, mid + 1, high)

    def getItem(self, idx: int) -> Activity:
        tmp = self.__getItem__(idx, 0, len(self.activities) - 1)
        return self.activities[tmp] if tmp == -1 else None


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
