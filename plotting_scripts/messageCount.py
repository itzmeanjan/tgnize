#!/usr/bin/python3

from __future__ import annotations
from model.chat import Chat
from typing import Dict

'''
    Returns a mapping of all those Users
    who're top contributors in this Chat,
    along with their percentage of contribution
    in terms of number of messages sent
'''

def getTopXParticipantsAlongWithContribution(x: int, chat: Chat) -> Dict[str, float]:
    _tmp = chat.totalMessageCount
    return dict(map(lambda e: (e, chat.getUser(e).totalMessageCount / _tmp * 100),
                    chat.getTopXParticipants(x)))



if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
