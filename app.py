#!/usr/bin/python3

from __future__ import annotations
from typing import List
from functools import reduce
from util import parseChat
from plot import extractMinuteBasedTraffic, extractMinuteBasedTrafficByUser, plotAccumulatedTrafficByMinuteFor24HourSpan

'''
    Main entry point of script
'''


def _getEscapedName(proposedName: str) -> str:
    return proposedName.translate(
        proposedName.maketrans(
            {'/': r'_',
             '\\': r'_',
             ' ': r'_',
             '\t': r'_',
             '\n': r'_',
             '\r': r'_'}
        )
    )


def __calculateSuccess__(data: List[bool]) -> float:
    return reduce(lambda acc, cur: (acc + 1) if cur else acc, data, 0) / len(data) * 100


def main() -> float:
    # a reusable reference, which will be used, over lifetime of this script,
    chat = parseChat()
    # holding full chat, under consideration
    _result = []
    _result.append(
        plotAccumulatedTrafficByMinuteFor24HourSpan(
            extractMinuteBasedTraffic(chat),
            'Accumulated Chat Traffic by Minute',
            './plots/accumulatedChatTrafficByMinute.jpg'
        )
    )
    for i in chat.users:
        _result.append(
            plotAccumulatedTrafficByMinuteFor24HourSpan(
                extractMinuteBasedTrafficByUser(chat, i.name),
                'Accumulated Chat Traffic by Minute for {}'.format(
                    i.name[:8] + '...' if len(i.name) > 10 else i.name),
                './plots/accumulatedChatTrafficByMinuteFor{}.jpg'.format(
                    _getEscapedName(i.name))
            )
        )
    return __calculateSuccess__(_result)


if __name__ == '__main__':
    try:
        print('[+]Success : {:.2f} %'.format(main()))
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
