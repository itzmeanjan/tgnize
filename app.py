#!/usr/bin/python3

from __future__ import annotations
from util import parseChat

'''
    Main entry point of script
'''


def main():
    print(parseChat())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
