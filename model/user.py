#!/usr/bin/python3

from __future__ import annotations
from typing import List, Dict
from itertools import chain

'''
    Holds record of messages sent by
    a chat participant, along with their identifying name
'''


class User:
    def __init__(self, name: str, messageIDs: List[int], viaBot: Dict[str, List[int]]):
        self.name = name
        self.messageIDs = messageIDs
        self.viaBotMessages = viaBot

    @property
    def messageCount(self) -> int:
        return len(self.messageIDs)

    @property
    def viaBotMessageCount(self) -> int:
        return sum([len(i) for i in self.viaBotMessages.values()])

    @property
    def totalMessageCount(self) -> int:
        return self.messageCount + self.viaBotMessageCount

    @property
    def getViaBotMessageIds(self) -> chain:
        return chain(*[i for i in self.viaBotMessages.values()])

    def updateViaBotMessages(self, botName: str, messageId: int):
        self.viaBotMessages[botName] = self.viaBotMessages.get(
            botName, []) + [messageId]


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
