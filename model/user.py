#!/usr/bin/python3

from __future__ import annotations
from typing import List

'''
    Holds record of messages sent by
    a chat participant, along with their identifying name
'''


class User:
    def __init__(self, name: str, messageIDs: List[int]):
        self.name = name
        self.messageIDs = messageIDs

    @property
    def messageCount(self):
        return len(self.messageIDs)


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
