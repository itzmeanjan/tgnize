#!/usr/bin/python3

from __future__ import annotations
from os import listdir
from os.path import join, abspath
from typing import List, Tuple
from model.chat import Chat
from model.message import Message
from model.event import Event
from re import compile as reg_compile
from time import time
try:
    from bs4 import BeautifulSoup
    from bs4.element import Tag
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def handleEvent(tag: Tag, chat: Chat):
    chat.push(
        Event(
            int(tag.get('id').replace('message', '')),
            tag.find('div', attrs={'class': 'body details'}).getText().strip()
        )
    )


def handleMessage(tag: Tag, chat: Chat, prev_tag: Tag = None):
    if not prev_tag:
        txt = tag.find('div', attrs={'class': 'text'})
        reply_to = tag.find(
            'div', attrs={'class': 'reply_to_details'})
        chat.push(
            Message(
                int(tag.get('id').replace('message', '')),
                tag.find('div', attrs={
                    'class': 'from_name'}).getText().strip(),
                txt.getText().strip() if txt else None,
                tag.find('div', attrs={'class': 'pull_right date details'}).get(
                    'title'),
                reply_to.a.get('href') if reply_to else None
            )
        )
    else:
        txt = prev_tag.find('div', attrs={'class': 'text'})
        chat.push(
            Message(
                int(tag.get('id').replace('message', '')),
                prev_tag.find('div', attrs={
                    'class': 'from_name'}).getText().strip(),
                txt.getText().strip() if txt else None,
                tag.find('div', attrs={'class': 'pull_right date details'}).get(
                    'title')
            )
        )


def routeToProperHandler(tag: Tag, prev_tag: Tag, chat: Chat) -> bool:
    if tag.get('class') == ['message', 'service']:
        handleEvent(tag, chat)
        return False
    elif tag.get('class') == ['message', 'default', 'clearfix']:
        handleMessage(tag, chat)
        return True
    else:
        handleMessage(tag, chat, prev_tag=prev_tag)
        return False


def buildAccumulatedActivitySet(acc: List[Tag], cur: List[Tag]):
    acc.extend(cur)
    return acc


'''
    Extracts all possible events happened in Chat,
    including message sent or people joined/ left
    in case of group chat.
'''


def getAllEvents(tree: BeautifulSoup) -> List[Tag]:
    reg = reg_compile(r'^(message[0-9]{1,})$')
    return [
        i
        for i in tree.findAll('div',
                              attrs={'class': 'message default clearfix'})
        +
        tree.findAll('div',
                     attrs={'class': 'message default clearfix joined'})
        +
        tree.findAll('div', attrs={'class': 'message service'})
        if reg.match(i.get('id'))
    ]


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
    target = []
    for i in getChatFiles(targetPath=targetPath):
        buildAccumulatedActivitySet(target,
                                    getAllEvents(
                                        BeautifulSoup(getFileContent(i), features='lxml')))
    last_msg_with_author = target[0]
    for i in target:
        if routeToProperHandler(i, last_msg_with_author, chat):
            last_msg_with_author = i
    return chat


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
