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

'''
    Pushes extracted message by a certain user
    into his/ her own record holder object.

    Along with so, updates main chat holder object
'''


def keepTrackOfMessages(user: str, message: Message, chat: Chat):
    check = chat.getUser(user)
    if not check:
        check = User(user, [message])
        chat.pushUser(check)
    else:
        check.messages.append(message)


'''
    Extracts message content from Div element
    of parsed html tree
'''


def parseAMessage(tag: Tag, idx: int) -> Tuple[str, Message]:
    txt = tag.find('div', attrs={'class': 'text'})
    return tag.find('div', attrs={'class': 'from_name'}).getText().strip(), \
        Message(
        idx,
        txt.getText().strip() if txt else None,
        tag.find('div', attrs={'class': 'pull_right date details'}).get(
            'title'))


'''
    Parses html content of a file, builds
    Element Tree, processes each message present
    with in that html file ( which is nothing but
    one of those exported chat files, present under ./data )
'''


def parseChatFile(content: str, idx: int, chat: Chat) -> int:
    tree = BeautifulSoup(content, features='lxml')
    for i, j in enumerate(tree.findAll('div',
                                       attrs={'class': 'message default clearfix'})):
        keepTrackOfMessages(*parseAMessage(j, idx + i), chat)
    return idx + i + 1


'''
    Reads whole content ( html file content)
    of requested filepath & return so
'''


def getFileContent(targetPath: str) -> str:
    with open(targetPath, mode='r') as fd:
        return fd.read()


'''
    Returns a collection of file paths
    which are holding exported telegram chat 
    ( i.e. group or private ), *.html files,
    present under ./data
'''


def getChatFiles(targetPath: str = './data') -> List[str]:
    return [join(abspath(targetPath), i)
            for i in listdir(targetPath)
            if i.startswith('messages') and i.endswith('html')]


'''
    Parses all exported telegram chat
    files ( html files ) and builds chat object,
    holding organized information regarding whole chat ( private/ group )
'''


def parseChat(targetPath: str = './data') -> Chat:
    chat = Chat([])
    tmp = 0
    for i in getChatFiles(targetPath=targetPath):
        tmp = parseChatFile(getFileContent(i), tmp, chat)
    return chat


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
