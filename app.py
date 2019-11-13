#!/usr/bin/python3

from __future__ import annotations
from typing import List
from functools import reduce
from util import parseChat
from plot import extractMinuteBasedTraffic, extractMinuteBasedTrafficByUser, plotAccumulatedTrafficByMinuteFor24HourSpan

'''
    Main entry point of script
'''


def __calculateSuccess__(data: List[bool]) -> float:
    return reduce(lambda acc, cur: (acc + 1) if cur else acc, data, 0) / len(data) * 100


def main() -> float:
    # a reusable reference, which will be used, over lifetime of this script,
    chat = parseChat()
    # holding full chat, under consideration
    return __calculateSuccess__(
        [
            plotAccumulatedTrafficByMinuteFor24HourSpan(
                extractMinuteBasedTraffic(chat),
                'Accumulated Chat Traffic by Minute',
                './plots/accumulatedChatTrafficByMinute.jpg'
            ),
            *map(lambda e:
                 plotAccumulatedTrafficByMinuteFor24HourSpan(
                     extractMinuteBasedTrafficByUser(chat, e.name),
                     'Accumulated Chat Traffic by Minute for {}'.format(
                         e.name),
                     './plots/accumulatedChatTrafficByMinuteFor{}.jpg'.format(
                         e.name)
                 ),
                 chat.users)
        ]
    )


if __name__ == '__main__':
    try:
        print('[+]Success : {:.2f} %'.format(main()))
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
