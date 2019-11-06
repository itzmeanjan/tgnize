#!/usr/bin/python3

from __future__ import annotations
from typing import List
from event import Event
from activity import Activity
from message import Message


class Chat:
    def __init__(self, activities: List[Activity]):
        self.activities = activities


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
