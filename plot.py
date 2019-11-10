#!/usr/bin/python3

from __future__ import annotations
from matplotlib import pyplot as plt
from matplotlib.dates import HourLocator, MinuteLocator, DateFormatter
from matplotlib.ticker import NullFormatter, NullLocator
from model.chat import Chat
from collections import Counter
from typing import Tuple
from datetime import datetime, date, time

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
        map(lambda e:
            e.getTime.replace(minute=(
                e.getTime.minute + 1) if e.getTime.minute < 59 else e.getTime.minute, second=0)
            if e.getTime.second >= 30
            else e.getTime.replace(second=0),
            filter(lambda e:
                   not chat.isEvent(e.index),
                   chat.activities
                   )
            )
    )


def determineHalveOfDay(tm: time) -> int:
    return 0 \
        if tm >= time(0, 0) and tm <= time(5, 59) else 1 \
        if tm >= time(6, 0) and tm <= time(11, 59) else 2 \
        if tm >= time(12, 0) and tm <= time(17, 59) else 3


def splitMinuteBasedTrafficIntoFourParts(traffic: Counter) -> Tuple[Counter]:
    first, second, third, fourth = Counter(
        []), Counter([]), Counter([]), Counter([])
    for i, j in traffic.items():
        _tmp = determineHalveOfDay(i)
        if _tmp == 0:
            first[datetime.combine(date(2000, 1, 1), i)] = j
        elif _tmp == 1:
            second[datetime.combine(date(2000, 1, 1), i)] = j
        elif _tmp == 2:
            third[datetime.combine(date(2000, 1, 1), i)] = j
        else:
            fourth[datetime.combine(date(2000, 1, 1), i)] = j
    return first, second, third, fourth


def plotAccumulatedTrafficByMinuteFor24HourSpan(data: Counter, targetPath: str) -> bool:
    first, second, third, fourth = splitMinuteBasedTrafficIntoFourParts(data)
    with plt.style.context('Solarize_Light2'):
        _, ((top_left, top_right), (bottom_left, bottom_right)) = plt.subplots(
            nrows=2, ncols=2, figsize=(24, 12), dpi=100)
        top_left.xaxis.set_major_locator(HourLocator())
        top_left.xaxis.set_major_formatter(DateFormatter('%I:%M %p'))
        top_left.xaxis.set_minor_locator(MinuteLocator())
        top_right.xaxis.set_major_locator(HourLocator())
        top_right.xaxis.set_major_formatter(DateFormatter('%I:%M %p'))
        top_right.xaxis.set_minor_locator(MinuteLocator())
        bottom_left.xaxis.set_major_locator(HourLocator())
        bottom_left.xaxis.set_major_formatter(DateFormatter('%I:%M %p'))
        bottom_left.xaxis.set_minor_locator(MinuteLocator())
        bottom_right.xaxis.set_major_locator(HourLocator())
        bottom_right.xaxis.set_major_formatter(DateFormatter('%I:%M %p'))
        bottom_right.xaxis.set_minor_locator(MinuteLocator())
        top_left.plot(first.keys(), first.values(), 'r-', lw=.5)
        top_right.plot(second.keys(), second.values(), 'r-', lw=.5)
        bottom_left.plot(third.keys(), third.values(), 'r-', lw=.5)
        bottom_right.plot(fourth.keys(), fourth.values(), 'r-', lw=.5)
        plt.tight_layout()
        plt.savefig(targetPath, bbox_inches='tight',
                    pad_inches=.2, quality=95, dpi=100)
        plt.close()
    return True


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
