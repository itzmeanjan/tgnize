#!/usr/bin/python3

from __future__ import annotations
from typing import List, Dict

'''
    Holds record of messages sent by
    a chat participant, along with their identifying name
'''


class User:
    def __init__(self, name: str, messageIDs: List[int] = [], viaBot: Dict[str, List[int]] = {}):
        self.name = name
        self.messageIDs = messageIDs
        self.viaBotMessages = viaBot

    @property
    def messageCount(self):
        return len(self.messageIDs)

    def updateViaBotMessages(self, botName: str, messageId: int):
        self.viaBotMessages[botName] = self.viaBotMessages.get(
            botName, []).append(messageId)


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
