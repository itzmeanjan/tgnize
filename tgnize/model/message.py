#!/usr/bin/python3

from __future__ import annotations
from typing import Tuple
from datetime import datetime, time
from math import ceil
from .activity import Activity

'''
    This class is designed to hold
    record of a certain message sent by
    some chat participant

    Holds index of message, which will be
    useful in understanding ordering of messages
    ( i.e. how were they sent into chat ), actual
    message content along with timestamp of message
    ( i.e. sending time of message )
'''


class Message(Activity):
    def __init__(self, idx: int, user: Tuple[str, str], content: str, timestamp: str, replyTo: int = None):
        super().__init__(idx)
        self.user, self.botName = user
        self.content = content
        self.timestamp = timestamp
        self.replyTo = replyTo

    @property
    def getDateTime(self) -> datetime:
        return datetime.strptime(self.timestamp, '%d.%m.%Y %H:%M:%S')

    '''
        Parses message timestamp and returns # of seconds
        from Epoch ( try searching, if you don't understand
        what's it )
    '''
    @property
    def getTimeStamp(self) -> int:
        return ceil(self.getDateTime.timestamp())

    @property
    def getTime(self) -> time:
        return self.getDateTime.time()


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
