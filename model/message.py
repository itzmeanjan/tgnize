#!/usr/bin/python3

from __future__ import annotations


class Message:
    def __init__(self, idx: int, content: str, timestamp: str):
        self.index = idx
        self.content = content
        self.timestamp = timestamp


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
