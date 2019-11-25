#!/usr/bin/python3

from __future__ import annotations
from matplotlib import pyplot as plt
from matplotlib import animation as anim
from matplotlib.dates import HourLocator, MinuteLocator, DateFormatter
from matplotlib.ticker import NullFormatter, NullLocator, MultipleLocator
from collections import Counter
from typing import Tuple
from datetime import datetime, date, time
from math import ceil
from itertools import chain
from ..model.chat import Chat
from ..model.plotDataRange import DataRange


def _fillUpEmptyMinuteSlotsWithZeroTrafficDenotation(traffic: Counter) -> Counter:
    if len(traffic.keys()) == 1440:
        return traffic
    else:
        for h in range(24):
            for m in range(60):
                _tmp = datetime.combine(date(2000, 1, 1), time(h, m, 0))
                traffic[_tmp] = traffic.get(_tmp, 0)
        return traffic


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
    return _fillUpEmptyMinuteSlotsWithZeroTrafficDenotation(
        Counter(
            map(lambda e:
                datetime.combine(date(2000, 1, 1),
                    e.getTime.replace(minute=(
                    e.getTime.minute + 1) if e.getTime.minute < 59 else e.getTime.minute, second=0)
                if e.getTime.second >= 30
                else e.getTime.replace(second=0)),
                filter(lambda e:
                       not chat.isEvent(e.index),
                       chat.activities
                       )
                )
        )
    )


'''
    Extracts all messages sent by a certain chat participant
    by its unique messageID & builds a frequency holder object,
    depicting how many messages sent by a certain user over an
    accumulated time period of a day ( i.e. 24 hours ), with minute level details.
'''


def extractMinuteBasedTrafficByUser(chat: Chat, user: str) -> Counter:
    userObj = chat.getUser(user)
    return _fillUpEmptyMinuteSlotsWithZeroTrafficDenotation(
        Counter(
            map(
                lambda e:
                datetime.combine(date(2000, 1, 1),
                e.getTime.replace(minute=(
                    e.getTime.minute + 1) if e.getTime.minute < 59 else e.getTime.minute, second=0)
                if e.getTime.second >= 30
                else e.getTime.replace(second=0)),
                chain(
                    map(lambda e:
                        chat.getActivity(e),
                        userObj.messageIDs),
                    map(lambda e: chat.getActivity(e),
                        userObj.getViaBotMessageIds)
                )
            )
        )
    )


def plotAnimatedGraphForAccumulatedTrafficByMinuteFor24HourSpan(data: Counter, title: str, targetPath: str) -> bool:
    def _calculateMaxLimitAlongY(val: int) -> int:
        return ceil(val + val / 10)

    def _animate(i: int):
        axes.clear()
        axes.xaxis.set_major_locator(HourLocator())
        axes.xaxis.set_major_formatter(DateFormatter('%I:%M %p'))
        #axes.xaxis.set_minor_locator(MinuteLocator())
        axes.set_ylim(-1, maxVal)
        axes.set_xlabel('Time', labelpad=12, fontdict={'size': 16})
        axes.set_ylabel('#-of Messages Sent', labelpad=12, fontdict={'size': 16})
        axes.set_title(title, pad=12)
        axes.tick_params(axis='x', which='major', labelsize=12, labelrotation=75, labelcolor='black')
        axes.tick_params(axis='y', which='major', labelsize=14, labelcolor='black')
        axes.plot(x[dataRange.getLow: (dataRange.getHigh + 1)],
                  y[dataRange.getLow: (dataRange.getHigh + 1)], linestyle='-',
                  color='tomato', linewidth=1.2, marker='o',
                  markerfacecolor='red', markersize=5)
        #dataRange.setLow(dataRange.getHigh)
        dataRange.setHigh((dataRange.getHigh + 60))

    try:
        x = sorted(data.keys())
        y = [data[i] for i in x]
        dataRange = DataRange(0, 59)
        maxVal = _calculateMaxLimitAlongY(max(y))
        with plt.style.context('Solarize_Light2'):
            fig = plt.figure(figsize=(24, 12), dpi=100)
            axes = fig.add_subplot(1, 1, 1)
            _anim = anim.FuncAnimation(fig, _animate, interval=1500, frames=24)
            _anim.save(targetPath, writer='imagemagick_file', dpi=100)
            plt.close(fig)
        return True
    except Exception:
        return False

'''
    For sake of ease I'm splitting a 24 hour
    lengthy day into 4 equal parts, which are as follows

    0 -> 00:00 - 05:59
    1 -> 06:00 - 11:59
    2 -> 12:00 - 17:59
    3 -> 18:00 - 23:59

    Now we need to map any HH:MM formatted
    time into one of those four halves, which will be
    indicated by 0 or 1 or 2 or 3
'''

'''
def determineHalveOfDay(tm: time) -> int:
    return 0 \
        if tm >= time(0, 0) and tm <= time(5, 59) else 1 \
        if tm >= time(6, 0) and tm <= time(11, 59) else 2 \
        if tm >= time(12, 0) and tm <= time(17, 59) else 3
'''

'''
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
'''

'''
def plotAccumulatedTrafficByMinuteFor24HourSpan(data: Counter, title: str, targetPath: str) -> bool:

    # currently not in use, will try to use in near future
    def _calculateMajorLocatorSpacingAlongX(minV: int, maxV: int, locatorCount: int = 5) -> int:
        return ceil((minV + maxV) / locatorCount)

    def _calculateMaxLimitAlongY(val: int) -> int:
        return ceil(val + val / 10)

    try:
        first, second, third, fourth = splitMinuteBasedTrafficIntoFourParts(
            data)
        x1 = sorted(first.keys())
        y1 = [first[i] for i in x1]
        x2 = sorted(second.keys())
        y2 = [second[i] for i in x2]
        x3 = sorted(third.keys())
        y3 = [third[i] for i in x3]
        x4 = sorted(fourth.keys())
        y4 = [fourth[i] for i in x4]
        maxVal = _calculateMaxLimitAlongY(
            max(max(y1), max(y2), max(y3), max(y4))
        )
        #_spaceBy = _calculateMajorLocatorSpacingAlongX(0, maxVal)
        with plt.style.context('Solarize_Light2'):
            _f, ((top_left, top_right), (bottom_left, bottom_right)) = plt.subplots(
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
            top_left.set_ylim(-1, maxVal)
            top_right.set_ylim(-1, maxVal)
            bottom_left.set_ylim(-1, maxVal)
            bottom_right.set_ylim(-1, maxVal)
            \'''
            top_left.yaxis.set_major_locator(MultipleLocator(_spaceBy))
            top_right.yaxis.set_major_locator(MultipleLocator(_spaceBy))
            bottom_left.yaxis.set_major_locator(MultipleLocator(_spaceBy))
            bottom_right.yaxis.set_major_locator(MultipleLocator(_spaceBy))
            \'''
            top_left.set_xlabel('Time', labelpad=12)
            top_left.set_ylabel('#-of Messages Sent', labelpad=12)
            top_right.set_xlabel('Time', labelpad=12)
            top_right.set_ylabel('#-of Messages Sent', labelpad=12)
            bottom_left.set_xlabel('Time', labelpad=12)
            bottom_left.set_ylabel('#-of Messages Sent', labelpad=12)
            bottom_right.set_xlabel('Time', labelpad=12)
            bottom_right.set_ylabel('#-of Messages Sent', labelpad=12)
            top_left.set_title(title, pad=12)
            top_right.set_title(title, pad=12)
            bottom_left.set_title(title, pad=12)
            bottom_right.set_title(title, pad=12)
            top_left.plot(x1, y1, linestyle='-',
                          color='tomato', linewidth=.5, marker='.', markerfacecolor='red', markersize=2)
            top_right.plot(x2, y2, linestyle='-',
                           color='tomato', linewidth=.5, marker='.', markerfacecolor='red', markersize=2)
            bottom_left.plot(x3, y3, linestyle='-',
                             color='tomato', linewidth=.5, marker='.', markerfacecolor='red', markersize=2)
            bottom_right.plot(x4, y4, linestyle='-',
                              color='tomato', linewidth=.5, marker='.', markerfacecolor='red', markersize=2)
            plt.tight_layout()
            plt.savefig(targetPath, bbox_inches='tight',
                        pad_inches=.2, quality=95, dpi=100)
            # this is really important, otherwise all figures will stay in memory
            plt.close(_f)
            # which will cause consumption of huge chunk of memory
        return True
    except Exception:
        return False
'''


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
