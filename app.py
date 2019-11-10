#!/usr/bin/python3

from __future__ import annotations
from typing import List
from functools import reduce
from util import parseChat
from plot import extractMinuteBasedTraffic, plotAccumulatedTrafficByMinuteFor24HourSpan

'''
    Main entry point of script
'''


def __calculateSuccess__(data: List[bool]) -> float:
    return reduce(lambda acc, cur: (acc + 1) if cur else acc, data, 0) / len(data) * 100


def main():
    return [
        plotAccumulatedTrafficByMinuteFor24HourSpan(
            extractMinuteBasedTraffic(parseChat()), './plots/accumulatedChatTrafficByMinute.jpg')
    ]


if __name__ == '__main__':
    try:
        print('[+]Success : {:.2f} %'.format(main()))
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
