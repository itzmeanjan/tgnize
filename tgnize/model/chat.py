#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple
from re import compile as reg_compile
from functools import reduce
from datetime import datetime, timedelta
from .activity import Activity
from .user import User


class Chat:

    def __init__(self, activities: List[Activity] = [], users: List[User] = []):
        self.activities = activities
        self.users = users
        self._activityCount = len(self.activities)
        self._userCount = len(self.users)

    '''
        Simply nothing but sum of self.totalMessageCount & self.totalEventCount,
        holding all activities happened in Chat, over period of data collection.
    '''

    @property
    def activityCount(self) -> int:
        return self._activityCount

    '''
        Returns # of users, who participated in this Chat
    '''

    @property
    def userCount(self) -> int:
        return self._userCount

    '''
        Calculates total # of messages, sent by chat participants
        into Chat, over period of data collection.
    '''

    @property
    def totalMessageCount(self) -> int:
        return reduce(lambda acc, cur: acc + (1 if not self.isEvent(cur.index) else 0), self.activities, 0)

    '''
        Calculates total # of events, happened in Chat, over
        period of data collection.
    '''

    @property
    def totalEventCount(self) -> int:
        return reduce(lambda acc, cur: acc + (1 if self.isEvent(cur.index) else 0), self.activities, 0)

    '''
        Gives us an iterator for traversing
        over an instance of Chat object
    '''

    def __iter__(self):
        return iter(self.activities)

    '''
        Returns position, at which we need to insert
        a new Activity ( for this chat ), so that
        ascendingly sorted order is kept.

        Position is found using binary search mechanism.
    '''

    def __getPushPosition__(self, idx: int, low: int, high: int):
        if low > high:
            return 0
        elif low == high:
            return low if self.activities[low].index >= idx else (low + 1)
        else:
            mid = low + (high - low) // 2
            if self.activities[mid].index == idx:
                return mid + 1
            else:
                return self.__getPushPosition__(idx, low, mid) \
                    if self.activities[mid].index > idx \
                    else self.__getPushPosition__(idx, mid + 1, high)

    '''
        Pushes an instance of Activity subclass ( either Event or Message )
        into collection of all activities happened in chat
        in proper position, so that sorted order is kept
        ( ascending in terms of index of Activity )
    '''

    def push(self, item: Activity):
        self.activities.insert(self.__getPushPosition__(
            item.index, 0, len(self.activities) - 1), item)
        self._activityCount += 1

    '''
        Denotes whether this activity is an Event
        or not

        If not an event, then it's a Message, sent by
        some chat participant
    '''

    def isEvent(self, idx: int) -> bool:
        try:
            self.getActivity(idx).user
            return False
        except Exception:
            return True

    '''
        As all entries made into chat holder are organized in
        sorted fashion in terms of their index number,
        we can reduce search time by doing it using interpolation search.

        That's what is done here.
    '''

    def __getActivity__(self, idx: int, low: int, high: int) -> int:
        if low > high:
            return -1
        elif low == high:
            return low if self.activities[low].index == idx else -1
        else:
            mid = low + \
                ((high - low) * (idx - self.activities[low].index)) \
                // (self.activities[high].index -
                    self.activities[low].index)
            if mid < low or mid > high:
                return -1
            if self.activities[mid].index == idx:
                return mid
            else:
                return self.__getActivity__(idx, low, mid - 1) \
                    if self.activities[mid].index > idx \
                    else self.__getActivity__(idx, mid + 1, high)

    '''
        Finds an activity ( may be event or message ),
        happened in group by its corresponding index value
        ( well this index is generated by telegram desktop
        application, while exporting chat, which is to be examined )
    '''

    def getActivity(self, idx: int) -> Activity:
        tmp = self.__getActivity__(idx, 0, len(self.activities) - 1)
        return self.activities[tmp] if tmp != -1 else None

    '''
        Helps in finding proper insertion position
        for an User object, so that self.users
        stays ascendingly sorted even after insertion at this
        position.

        This position finding is done using recursive mechanism ( binary search )
    '''

    def __pushUserPosition__(self, user: str, low: int, high: int):
        if low > high:
            return 0
        elif low == high:
            return low if self.users[low].name > user else (low + 1)
        else:
            mid = (low + high) // 2
            return self.__pushUserPosition__(user, low, mid) \
                if self.users[mid].name > user \
                else self.__pushUserPosition__(user, mid + 1, high)

    '''
        Pushes an User object into self.users,
        such that they list stays ascendingly sorted
        by user names.
    '''

    def pushUser(self, user: User):
        self.users.insert(self.__pushUserPosition__(
            user.name, 0, len(self.users) - 1), user)
        self._userCount += 1

    '''
        Finds an User object by its name,
        in recursive fashion, using binary search mechanism.

        Cause self.users is always kept sorted in ascending fashion
        by user names.
    '''

    def __getUser__(self, user: str, low: int, high: int):
        if low > high:
            return -1
        elif low == high:
            return low if self.users[low].name == user else -1
        else:
            mid = (low + high) // 2
            return self.__getUser__(user, low, mid) \
                if self.users[mid].name >= user \
                else self.__getUser__(user, mid + 1, high)

    '''
        Looks up an User object by user name,
        if it's present in self.records,
        we simply return that object,
        other wise we return None, denoting failure.
    '''

    def getUser(self, user: str) -> User:
        _tmp = self.__getUser__(user, 0, len(self.users) - 1)
        return self.users[_tmp] if _tmp != -1 else None

    '''
        In the method, immediately below of it, we tried
        understanding whether this message is via any bot or not.

        If yes, we go for extraction of two important
        components

        `x via @y` i.e. `x` = username & `y` = botname

        We'll use a regex for that purpose, and a tuple
        holding both of them ( of course in ordered fashion ),
        is to be returned

        Before invoking this method, make sure you're getting true
        by invoking method, placed just below it.
    '''

    def extractUserAndBotNameFromMessage(self, username: str) -> Tuple[str, str]:
        regex = reg_compile(r'(.+)(?=\svia\s)\svia\s(.+)')
        return regex.search(username).groups()

    '''
        Checks whether this message is sent by using any bot or not,
        mostly gifs or other kind of memes are sent via different telegram bots.

        In those cases, username is like

        `x via @y`, where `x` is actual user account name & `y` is botname

        If that's the case for this message, we'll return True,
        else False, to be returned.
    '''

    def isAViaBotMessage(self, username: str) -> bool:
        regex = reg_compile(r'(.+)(?=\svia\s)\svia\s(.+)')
        return True if regex.search(username) else False

    '''
        Takes an user ( indentifying ) name & a message id,
        denoting that message is sent by that user,
        and tries to lookup an User object with
        that username.

        Now there may be two conditions

        Either User object with that name is already exisiting,
        in that case, we simply update its messageID container list,
        while pushing this one.

        Or we need to create an User object with that name,
        along with this messageID, and push that into proper
        place while maintaining ascendingly sorted order of Users,
        into self.users : List[User]
    '''

    def updateUserRecords(self, user: str, messageID: int):
        if self.isAViaBotMessage(user):
            userName, botName = self.extractUserAndBotNameFromMessage(user)
            _tmp = self.getUser(userName)
            if not _tmp:
                _tmpUser = User(userName, [], {})
                _tmpUser.updateViaBotMessages(botName, messageID)
                self.pushUser(_tmpUser)
            else:
                _tmp.updateViaBotMessages(botName, messageID)
        else:
            _tmp = self.getUser(user)
            if not _tmp:
                _tmpUser = User(user, [], {})
                _tmpUser.pushMessageId(messageID)
                self.pushUser(_tmpUser)
            else:
                _tmp.pushMessageId(messageID)

    '''
        Get Top X chat contributors name list,
        in terms of #-of messages sent by them in Chat
    '''

    def getTopXParticipants(self, x: int) -> List[str]:
        return [i.name for i in sorted(self.users, key=lambda e: e.totalMessageCount, reverse=True)[:x]]

    '''
        Get a list of those users who
        ever sent any message via bot
        to this Chat
    '''

    def getUsersWhoUsedBot(self) -> List[str]:
        return [i.name for i in filter(lambda e: e.sentAnyMessageViaBot, self.users)]

    '''
        Returns count of those users who
        sent any message to this Chat via bot
    '''

    def getUserCountWhoUsedBot(self) -> int:
        return len(self.getUsersWhoUsedBot())

    '''
        Returns a list of those users who
        never sent any message via bot to this Chat
    '''

    def getUsersWhoDidNotUseBot(self) -> List[str]:
        return [i.name for i in filter(lambda e: not e.sentAnyMessageViaBot, self.users)]

    '''
        Returns count of aforementioned kind of users
    '''

    def getUserCountWhoDidNotUseBot(self) -> int:
        return len(self.getUsersWhoDidNotUseBot())

    @property
    def _findFirstMessage(self) -> Message:
        _tmp = None
        for i in self.activities:
            if not self.isEvent(i.index):
                _tmp = i
                break
        return _tmp

    @property
    def _findLastMessage(self) -> Message:
        _tmp = None
        for i in range(self.activityCount - 1, -1, -1):
            if not self.isEvent(self.activities[i].index):
                _tmp = self.activities[i]
                break
        return _tmp

    def getChatTimeRange(self) -> Tuple[datetime, datetime]:
        return self._findFirstMessage.getDateTime, self._findLastMessage.getDateTime

    def splitTimeRangeWithGap(self, timeRange: Tuple[datetime, datetime], gap: timedelta) -> List[Tuple[datetime, datetime]]:
        _tmp = []
        _a = timeRange[0]
        _b = _a + gap
        while(_b < timeRange[1]):
            _tmp.append((_a, _b))
            _a = _b + timedelta(seconds = 1)
            _b = _a + gap
        _tmp.append((_a, timeRange[1]))
        return _tmp

    def findActivitiesWithInTimeRange(self, timeRange: Tuple[datetime, datetime]) -> List[int]:
        _tmp = []
        for i in self.activities:
            if not self.isEvent(i.index):
                if timeRange[0] <= i.getDateTime <= timeRange[1]:
                    _tmp.append(i.index)
                if i.getDateTime > timeRange[1]:
                    break
        return _tmp

    '''
        Returns a 3 element tuple, indicating minimum delay,
        maximum delay & average delay between two messages,
        sent one immediately after another, while considering those
        messages only sent within given time range.
    '''

    def delayInMessagesWithInTimeRange(self, timeRange: Tuple[datetime, datetime]) -> Tuple(timedelta, timedelta, timedelta):
        _tmp = self.findActivitiesWithInTimeRange(timeRange)
        _tot = timedelta()
        _maxDelay = self.getActivity(_tmp[1]).getDateTime - self.getActivity(_tmp[0]).getDateTime
        _minDelay = _maxDelay
        for i, j in enumerate(_tmp):
            try:
                _cur = (self.getActivity(_tmp[i + 1]).getDateTime - self.getActivity(j).getDateTime)
                _tot += _cur
                if _maxDelay < _cur:
                    _maxDelay = _cur
                if _minDelay > _cur:
                    _minDelay = _cur
            except IndexError:
                pass
        return _minDelay, _maxDelay, _tot / (len(_tmp) - 1)

    def _findUserWildCard(self, low: int, high: int, name: str, found : List[str]):
        if low > high:
            return
        elif low == high:
            if self.users[low].name.startswith(name):
                found.append(self.users[low].name)
        else:
            mid = low + (high - low) // 2
            self._findUserWildCard(low, mid, name, found) if self.users[mid].name >= name \
                else self._findUserWildCard(mid + 1, high, name, found)

    def findUserWildCard(self, name: str) -> List[str]:
        _found = []
        self._findUserWildCard(0, self.userCount - 1, name, _found)
        return _found


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
