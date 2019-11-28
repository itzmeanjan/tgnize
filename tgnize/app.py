#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple
from functools import reduce
from subprocess import run
from sys import argv
from os import mkdir
from os.path import abspath, exists, join
from datetime import timedelta
from .util import parseChat
from .plotting_scripts.minuteBasedAccumulatedTraffic import (
    extractMinuteBasedTraffic,
    extractMinuteBasedTrafficByUser,
    plotAnimatedGraphForAccumulatedTrafficByMinuteFor24HourSpan,
    calculateChatTrafficPercentageInPartOfDay
)
from .plotting_scripts.activeParticipantsOverTime import (
    getTopXParticipantsAlongWithContribution,
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
    print('\x1b[1;6;36;49m[+]tgnize v0.1.3 - How about another Telegram Chat Analyzer ?\x1b[0m\n\n\t\x1b[3;30;47m$ tgnize `path-to-exported-chat-dir` `path-to-sink-dir`\x1b[0m\n\n[+]Author: Anjan Roy<anjanroy@yandex.com>\n[+]Source: \x1b[4mhttps://github.com/itzmeanjan/tgnize\x1b[0m ( MIT Licensed )\n')

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
    return 0.0 if not data else reduce(lambda acc, cur: (acc + 1) if cur else acc, data, 0) / len(data) * 100

def _choiceHandler(ch: int, chat: Chat):
    if ch == -1 or ch == 10:
        print('\n[!]Terminated')
        exit(0)
    elif ch == 0:
        print('\n\x1b[5;31;49m[!]Invalid choice\x1b[0m')
    elif ch == 1:
        print('\nFound \x1b[1;31;49m{}\x1b[0m participants in Chat'.format(chat.userCount))
    elif ch == 2:
        print('\nFound \x1b[1;31;49m{}\x1b[0m messages in Chat'.format(chat.totalMessageCount))
    elif ch == 3:
        print('\nFound \x1b[1;31;49m{}\x1b[0m events in Chat'.format(chat.totalEventCount))
    elif ch == 4:
        print('\nFound \x1b[1;31;49m{}\x1b[0m activities in Chat ( in total )'.format(chat.activityCount))
    elif ch == 5:
        try:
            print('\n`X` > ', end='')
            print('{}'.format(''.join(['\n{} - \x1b[1;3;34;50m{}\x1b[0m ( {:.4f} % )'.format(i + 1, k, v) for i, (k, v) in enumerate(getTopXParticipantsAlongWithContribution(int(input()), chat).items())])))
        except Exception:
            print('\n[!]Bad Input')
    elif ch == 6:
        _from, _to = chat.getChatTimeRange()
        print('\nFrom \x1b[3;31;50m{}\x1b[0m to \x1b[3;31;50m{}\x1b[0m\nSpans over : \x1b[3;33;50m{}\x1b[0m'.format(_from, _to, _to - _from))
    elif ch == 7:
        _tmp = chat.getUserCountWhoUsedBot()
        print('\nFound \x1b[1;31;49m{}\x1b[0m ( {:.4f} % ) participants who sent message via Bot'.format(_tmp, _tmp * 100 / chat.userCount))
    elif ch == 8:
        _tmp = chat.getUserCountWhoDidNotUseBot()
        print('\nFound \x1b[1;31;49m{}\x1b[0m ( {:.4f} % ) participants who didn\'t send message via Bot'.format(_tmp, _tmp * 100 / chat.userCount))
    elif ch == 9:
        print(''.join(['\n\x1b[1;3;34;50m{}\x1b[0m ( {:.4f} % )'.format(k, v) for k, v in calculateChatTrafficPercentageInPartOfDay(chat).items()]))
    else:
        print('\n\x1b[1;6;36;49m\_(^-^)_/\x1b[0m')

def _menu() -> int:
    try:
        print("\n[+]Options ::\n\n\t1 > Get Chat Participant Count\n\t2 > Get Message Count in Chat\n\t3 > Get Event Count in Chat\n\t4 > Get Total Activity Count in Chat\n\t5 > Get Top `X` Chat Participant(s)\n\t6 > Get Time Range of Chat\n\t7 > Get participant count, who sent message via Bot\n\t8 > Get participant count, who didn't send message via Bot\n\t9 > Accumulated Chat traffic in parts of Day\n\t10 > Exit\n\n\x1b[1;1;32;50mtgnize >> \x1b[0m", end="")
        return int(input())
    except EOFError:
        return -1
    except Exception:
        return 0

'''
    Main entry point of script
'''


def main() -> float:
    run('clear')
    _result = []
    try:
        source, sink = _handleCMDInput()
        if not source or not sink or not exists(source):
            _displayBanner()
            raise Exception('Improper Invocation of `tgnize`')
        _sinkDirBuilder(sink)
        _displayBanner()
        print('[*]Preparing ...')
        # a reusable reference, which will be used, over lifetime of this script,
        chat = parseChat(source)
        # holding full chat, currently under consideration
        while(1):
            _choiceHandler(_menu(), chat)
        '''
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
    except KeyboardInterrupt:
        print('[!]Terminated')
    except Exception as e:
        print('[!]{}'.format(e))
    '''
    finally:
        print('[+]Success : {:.2f} %'.format(__calculateSuccess__(_result)))
    '''


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
