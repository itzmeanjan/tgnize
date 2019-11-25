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
        self._messageIDs = messageIDs
        self.viaBotMessages = viaBot

    @property
    def messageIDs(self) -> List[int]:
        return self._messageIDs

    @property
    def messageCount(self) -> int:
        return len(self._messageIDs)

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

    def __push__(self, low: int, high: int, msgId: int):
        if low > high:
            return 0
        elif low == high:
            return low if self._messageIDs[low] > msgId else (low + 1)
        else:
            mid = low + (high - low) // 2
            return self.__push__(low, mid, msgId) if self._messageIDs[mid] > msgId \
                else self.__push__(mid + 1, high, msgId)

    def pushMessageId(self, msgId: int):
        self._messageIDs.insert(self.__push__(0, len(self._messageIDs) - 1, msgId), msgId)

    '''
        Simply denotes whether this User has ever
        sent any message via bot(s) or not ( in this Chat ),
        by a boolean value
    '''
    @property
    def sentAnyMessageViaBot(self):
        return self.viaBotMessageCount != 0


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
