#!/usr/bin/python3

from __future__ import annotations
from ..model.chat import Chat
from typing import Dict
from matplotlib import pyplot as plt
from matplotlib import animation as anim
from matplotlib.ticker import PercentFormatter
from collections import Counter

'''
    Returns a mapping of all those Users
    who're top contributors in this Chat,
    along with their percentage of contribution
    in terms of number of messages sent
'''

def getTopXParticipantsAlongWithContribution(x: int, chat: Chat) -> Dict[str, float]:
    _tmp = chat.totalMessageCount
    return dict(map(lambda e: (e, chat.getUser(e).totalMessageCount / _tmp * 100),
                    chat.getTopXParticipants(x)))


def getTopXParticipantsFromMessageRangeAlongWithContribution(x: int, chat: Chat, msgIds: List[int]) -> Dict[str, float]:
    _users = [chat.getActivity(i).user for i in msgIds]
    _msgCount = len(_users)
    return dict([(i, j / _msgCount * 100) for i, j in Counter(_users).most_common(x)])

def plotAnimatedGraphShowingTopXActiveParticipantsOverTime(data: List[Tuple[str, Dict[str, float]]], targetPath: str) -> bool:

    def _animate(i: int):
        _title, _dataForTimeRange = data[i]
        _x = [i for i in _dataForTimeRange]
        _y = [_dataForTimeRange.get(i) for i in _x]
        axes.clear()
        axes.xaxis.set_major_formatter(PercentFormatter())
        axes.set_title(_title, pad=16)
        axes.tick_params(axis='x', which='major', labelsize=14, labelcolor='black')
        axes.tick_params(axis='y', which='major', labelsize=16, labelcolor='black')
        axes.barh(range(len(_x)), _y, tick_label=_x, color='steelblue', align='center')
        return

    try:
        with plt.style.context('Solarize_Light2'):
            fig = plt.figure(figsize=(24, 12), dpi=100)
            axes = fig.add_subplot(1, 1, 1)
            _anim = anim.FuncAnimation(fig, _animate, interval=2000, frames=len(data))
            _anim.save(targetPath, writer='imagemagick_file', dpi=100)
            plt.close(fig)
        return True
    except Exception:
        return False

if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
