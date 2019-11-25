#!/usr/bin/python3

from __future__ import annotations
from .activity import Activity


class Event(Activity):
    def __init__(self, idx: int, details: str):
        super().__init__(idx)
        self.details = details


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
