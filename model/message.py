#!/usr/bin/python3

from __future__ import annotations
from datetime import datetime
from activity import Activity

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
    def __init__(self, idx: int, user: str, content: str, timestamp: str):
        super().__init__(idx)
        self.user = user
        self.content = content
        self.timestamp = timestamp

    '''
        Parses message timestamp and returns # of seconds
        from Epoch ( try searching, if you don't understand
        what's it )
    '''
    @property
    def parseTimeStamp(self) -> int:
        return datetime.strptime(self.timestamp, '%d.%m.%Y %H:%M:%S').timestamp()


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
