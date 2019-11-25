#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple
from functools import reduce
from sys import argv
from os import mkdir
from os.path import abspath, exists, join
from datetime import timedelta
from .util import parseChat
from .plotting_scripts.minuteBasedAccumulatedTraffic import (
    extractMinuteBasedTraffic,
    extractMinuteBasedTrafficByUser,
    plotAnimatedGraphForAccumulatedTrafficByMinuteFor24HourSpan
)
from .plotting_scripts.activeParticipantsOverTime import (
    getTopXParticipantsFromMessageRangeAlongWithContribution,
    plotAnimatedGraphShowingTopXActiveParticipantsOverTime
)


'''
    Given sink directory path and target file name,
    it joins them into a single component & returns
    sink file path ( absolute )
'''

def _getSinkFilePath(dirName: str, fileName: str) -> str:
    return join(abspath(dirName), fileName)

'''
    Checks presence of sink directory on current machine,
    if doesn't exists, it builds so.
'''

def _sinkDirBuilder(targetPath: str):
    _tmp = abspath(targetPath)
    if not exists(_tmp):
        mkdir(_tmp)

'''
    Displays a simple banner, depicting usage of script,
    along with author name & repository address
'''

def _displayBanner():
    print('\x1b[1;6;36;49m[+]tgnize v0.1.1 - How about another Telegram Chat Analyzer ?\x1b[0m\n\n\t\x1b[3;30;47m$ tgnize `path-to-exported-chat-dir` `path-to-sink-dir`\x1b[0m\n\n[+]Author: Anjan Roy<anjanroy@yandex.com>\n[+]Source: https://github.com/itzmeanjan/tgnize ( MIT Licensed )\n')

'''
    Retuns source directory path ( holding exported telegram chat data set ) &
    sink directory ( where we'll store generated plots )
'''

def _handleCMDInput() -> Tuple[str, str]:
    return tuple(argv[1:len(argv)]) if len(argv) == 3 else (None, None)

'''
    Escapes troublesome special characters present in chat participant's
    names, which might cause some issue, if we put it in generated plots ( animated )
    name
'''

def _getEscapedName(proposedName: str) -> str:
    return proposedName.translate(
        proposedName.maketrans(
            {'/': r'_',
             '\\': r'_',
             ' ': r'_'
             }
        )
    )

'''
    Calculates rate of success of execution of this script on
    exported chat data
'''

def __calculateSuccess__(data: List[bool]) -> float:
    try:
        return reduce(lambda acc, cur: (acc + 1) if cur else acc, data, 0) / len(data) * 100
    except Exception:
        return 0.0 # for safety, if we get a empty list as input, it'll raise DivisionByZero error, which will be caught


'''
    Main entry point of script
'''


def main() -> float:
    _result = []
    try:
        source, sink = _handleCMDInput()
        if not source or not sink or not exists(source):
            _displayBanner()
            raise Exception('Improper Invocation of `tgnize`')
        _sinkDirBuilder(sink)
        print('\x1b[1;6;36;49m[+]tgnize v0.1.1 - How about another Telegram Chat Analyzer ?\x1b[0m\n[*]Working ...')
        # a reusable reference, which will be used, over lifetime of this script,
        chat = parseChat(source)
        # holding full chat, currently under consideration
        _result.append(
            plotAnimatedGraphForAccumulatedTrafficByMinuteFor24HourSpan(
                extractMinuteBasedTraffic(chat),
                'Accumulated Chat Traffic by Minute',
                _getSinkFilePath(sink, 'accumulatedChatTrafficByMinute.gif')
            )
        )
        for i in chat.getTopXParticipants(5):
            _result.append(
                plotAnimatedGraphForAccumulatedTrafficByMinuteFor24HourSpan(
                    extractMinuteBasedTrafficByUser(chat, i),
                    'Accumulated Chat Traffic by Minute for {}'.format(i),
                    _getSinkFilePath(sink, 'accumulatedChatTrafficByMinuteFor{}.gif'.format(
                    _getEscapedName(i)))
                )
            )
        _result.append(
            plotAnimatedGraphShowingTopXActiveParticipantsOverTime(
                [('Top 5 Active Participants from {} to {}'.format(i[0].strftime('%b %d %Y, %I:%M:%S %p'), i[1].strftime('%b %d %Y, %I:%M:%S %p')), \
                    getTopXParticipantsFromMessageRangeAlongWithContribution(5, chat, chat.findActivitiesWithInTimeRange(i))) \
                        for i in chat.splitTimeRangeWithGap(chat.getChatTimeRange(), timedelta(days=30))],
                _getSinkFilePath(sink, 'topXActiveChatParticipantsOverTime.gif')
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
    except Exception as e:
        print('[!]Error : {}'.format(e))
    finally:
        return __calculateSuccess__(_result)


if __name__ == '__main__':
    try:
        print('[+]Success : {:.2f} %'.format(main()))
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
