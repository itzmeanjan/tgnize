#!/usr/bin/python3

from __future__ import annotations


class Message:
    def __init__(self, timestamp: str, content: str):
        self.timestamp = timestamp
        self.content = content


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
