#!/usr/bin/python3

from __future__ import annotations


class DataRange:
    def __init__(self, low: int, high: int):
        self._low = low
        self._high = high

    @property
    def getLow(self) -> int:
        return self._low

    @property
    def getHigh(self) -> int:
        return self._high

    def setHigh(self, high: int):
        self._high = high % 1440 if high > 1439 else high


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
