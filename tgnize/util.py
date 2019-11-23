#!/usr/bin/python3

from __future__ import annotations
from os import listdir
from os.path import join, abspath
from typing import List, Tuple
from re import compile as reg_compile
from time import time

try:
    from bs4 import BeautifulSoup
    from bs4.element import Tag
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)

from .model.chat import Chat
from .model.message import Message
from .model.event import Event


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
        fromUser = tag.find('div', attrs={
            'class': 'from_name'}).getText().strip()
        chat.push(
            Message(
                int(tag.get('id').replace('message', '')),
                chat.extractUserAndBotNameFromMessage(fromUser) if chat.isAViaBotMessage(fromUser) else (fromUser, None),
                txt.getText().strip() if txt else None,
                tag.find('div', attrs={'class': 'pull_right date details'}).get(
                    'title'),
                int(reply_to.a.get('href')) if reply_to else None
            )
        )
        chat.updateUserRecords(
            fromUser,
            int(tag.get('id').replace('message', '')))
    else:
        txt = prev_tag.find('div', attrs={'class': 'text'})
        fromUser = prev_tag.find('div', attrs={
            'class': 'from_name'}).getText().strip()
        chat.push(
            Message(
                int(tag.get('id').replace('message', '')),
                chat.extractUserAndBotNameFromMessage(fromUser) if chat.isAViaBotMessage(fromUser) else (fromUser, None),
                txt.getText().strip() if txt else None,
                tag.find('div', attrs={'class': 'pull_right date details'}).get(
                    'title')
            )
        )
        chat.updateUserRecords(
            fromUser,
            int(tag.get('id').replace('message', '')))


'''
    Passes an extracted tag value to
    one handler function, which
    can handle this activity by
    considering it either
'''


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


'''
    Extracts all possible activities happened in Chat,
    including message sent or people joined/ left
    in case of group chat etc.

    And returns a list of those tags.
'''


def getAllActivities(tree: BeautifulSoup) -> List[Tag]:
    reg = reg_compile(r'^(message[0-9]{1,})$')
    tmp = tree.findAll('div',
                       attrs={'class': 'message default clearfix'})
    tmp.extend(tree.findAll('div',
                            attrs={'class': 'message default clearfix joined'}))
    tmp.extend(
        [
            i
            for i in tree.findAll('div', attrs={'class': 'message service'})
            if reg.match(i.get('id'))
        ]
    )
    return tmp


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


def getChatFiles(targetPath: str) -> List[str]:
    return [join(abspath(targetPath), i)
            for i in listdir(targetPath)
            if i.startswith('messages') and i.endswith('html')]


'''
    Parses all exported telegram chat
    files ( html files ) and builds chat object,
    holding organized information regarding whole chat ( private/ group )
'''


def parseChat(targetPath: str) -> Chat:
    chat = Chat()
    last_msg_with_author = None
    for i in getChatFiles(targetPath):
        for j in getAllActivities(BeautifulSoup(getFileContent(i), features='lxml')):
            if routeToProperHandler(j, last_msg_with_author, chat):
                last_msg_with_author = j
    return chat


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
