#!/usr/bin/python3

from __future__ import annotations
from typing import List


class User:
    def __init__(self, name: str, messageIDs: List[int]):
        self.name = name
        self.messageIDs = messageIDs


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
