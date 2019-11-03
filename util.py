#!/usr/bin/python3

from __future__ import annotations
from os import listdir
from os.path import join, abspath
from typing import List, Tuple
from model.message import Message
from model.chat import Chat
from model.user import User
try:
    from bs4 import BeautifulSoup
    from bs4.element import Tag
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def keepTrackOfMessages(user: str, message: Message, chat: Chat):
    check = chat.getUser(user)
    if not check:
        check = User(user, [message])
        chat.pushUser(check)
    else:
        check.messages.append(message)


def parseAMessage(tag: Tag, idx: int) -> Tuple[str, Message]:
    txt = tag.find('div', attrs={'class': 'text'})
    return tag.find('div', attrs={'class': 'from_name'}).getText().strip(), \
        Message(
        idx,
        txt.getText().strip() if txt else None,
        tag.find('div', attrs={'class': 'pull_right date details'}).get(
            'title'))


def parseChatFile(content: str, idx: int, chat: Chat) -> int:
    tree = BeautifulSoup(content, features='lxml')
    for i, j in enumerate(tree.findAll('div',
                                       attrs={'class': 'message default clearfix'})):
        keepTrackOfMessages(*parseAMessage(j, idx + i), chat)
    return idx + i + 1


def getFileContent(targetPath: str) -> str:
    with open(targetPath, mode='r') as fd:
        return fd.read()


def getChatFiles(targetPath: str = './data') -> List[str]:
    return [join(abspath(targetPath), i)
            for i in listdir(targetPath)
            if i.startswith('messages') and i.endswith('html')]


def parseChat(targetPath: str = './data') -> Chat:
    chat = Chat([])
    tmp = 0
    for i in getChatFiles(targetPath=targetPath):
        tmp = parseChatFile(getFileContent(i), tmp, chat)
    return chat


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
