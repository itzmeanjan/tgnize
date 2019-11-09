#!/usr/bin/python3

from __future__ import annotations
from matplotlib import pyplot as plt
from model.chat import Chat
from collections import Counter

'''
    Takes an instance of Chat class, 
    holding whole chat ( may be private or group ),
    to be analyzed. 
    
    First filters out those Activity
    subclasses which are not Message instances ( more
    specifically Event objects are put away, so that we
    can only concentrate into Message objects ). 

    Now time to map each Message object into
    its time of sending ( only time, currently I don't want date 
    involvement here, may be sometime in future I'll consider having so ).

    What do we get ?

    A collection of time objects ( imported from datetime module in python )
    holding time of sending of all messages into Chat, which is to be sent
    through Counter class, so that we get an instance of Counter object.

    Now we've a dictionary holding, at which minute of day, 
    how many messages are sent, giving us an accumulated overview
    of message sending trend of participants of this Chat.
'''


def extractMinuteBasedTraffic(chat: Chat) -> Counter:
    return Counter(
        map(lambda e: e.getTime.replace(second=0),
            filter(lambda e:
                   not chat.isEvent(e.index),
                   chat.activities
                   )
            )
    )


def plotAccumulatedTrafficByMinuteFor24HourSpan(data: Counter) -> bool:
    pass


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
