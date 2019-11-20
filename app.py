#!/usr/bin/python3

from __future__ import annotations
from typing import List
from functools import reduce
from util import parseChat
from plotting_scripts.minuteBasedAccumulatedTraffic import extractMinuteBasedTraffic, extractMinuteBasedTrafficByUser, plotAnimatedGraphForAccumulatedTrafficByMinuteFor24HourSpan


def _getEscapedName(proposedName: str) -> str:
    return proposedName.translate(
        proposedName.maketrans(
            {'/': r'_',
             '\\': r'_',
             ' ': r'_'
             }
        )
    )


def __calculateSuccess__(data: List[bool]) -> float:
    return reduce(lambda acc, cur: (acc + 1) if cur else acc, data, 0) / len(data) * 100


'''
    Main entry point of script
'''


def main() -> float:
    # a reusable reference, which will be used, over lifetime of this script,
    chat = parseChat()
    # holding full chat, under consideration
    _result = []
    _result.append(
        plotAnimatedGraphForAccumulatedTrafficByMinuteFor24HourSpan(
            extractMinuteBasedTraffic(chat),
            'Accumulated Chat Traffic by Minute',
            './plots/accumulatedChatTrafficByMinute.gif'
        )
    )
    for i in chat.getTopXParticipants(5):
        _result.append(
            plotAnimatedGraphForAccumulatedTrafficByMinuteFor24HourSpan(
                extractMinuteBasedTrafficByUser(chat, i),
                'Accumulated Chat Traffic by Minute for {}'.format(i),
                './plots/accumulatedChatTrafficByMinuteFor{}.gif'.format(
                    _getEscapedName(i))
            )
        )
    '''
    for i in chat.users:
        _result.append(
            plotAnimatedGraphForAccumulatedTrafficByMinuteFor24HourSpan(
                extractMinuteBasedTrafficByUser(chat, i.name),
                'Accumulated Chat Traffic by Minute for {}'.format(
                    i.name[:8] + '...' if len(i.name) > 10 else i.name),
                './plots/accumulatedChatTrafficByMinuteFor{}.gif'.format(
                    _getEscapedName(i.name))
            )
        )
    '''
    return __calculateSuccess__(_result)


if __name__ == '__main__':
    try:
        print('[+]Success : {:.2f} %'.format(main()))
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
