#!/usr/bin/python3

from __future__ import annotations
from typing import List
from message import Message


class User:
    def __init__(self, name: str, messages: List[Message]):
        self.name = name
        self.messages = messages


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
