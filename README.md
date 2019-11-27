# tgnize

![accumulatedChatTrafficByMinuteOfDevsChatGroupTelegram](./plots/accumulatedChatTrafficByMinute.gif)

How about another exported Telegram Chat analyzer ? :wink:

## nomenclature
Telegram + _( Chat )_ Analyze = tgnize

## motivation
- I'm always interested in learning more about data, which is why I thought about taking a deeper look into Telegram Chats _( mostly groups )_, I participate in.
- I exported chat data _( excluding audios, videos and images etc. )_, of [Devs Chat](https://t.me/joinchat/BkBvqUQUj4VKPmFSSNPQSw) group, using Telegram Desktop Client, which are nothing but some HTML, CSS & JS files
- I created an object model, into which I populated parsed Chat data, so that I can manipulate it well
- Then I started plotting animated charts & much more _( a lot of work remaining though )_, to depict how participants contributed to chat
- It also lets me understand my chat activity pattern(s) i.e. in which hour of the day I'm mostly active / inactive in Chat
- Or how another peer is spending their time is Chat
- What's mostly used words / mostly used bots / mostly used Emoji etc. in Chat

## caution
This project doesn't expect you to use any exported Chat for manipulating any participant or use extracted data _( sleep patterns, daily activity pattern of participants )_ for doing some harmful activity to any participant.

**If users use it for malicious purpose(s), it's not author's responsibility !!!**

I suggest you not to use it for manipulating someone else. Thank you for understanding :wink:

## data source
Here I'm using [Devs Chat](https://t.me/joinchat/BkBvqUQUj4VKPmFSSNPQSw)'s, exported Chat data set for testing these scripts. So all plots ( to be :wink: ) generated, present in this repository, are result of application of scripts on [Devs Chat](https://t.me/joinchat/BkBvqUQUj4VKPmFSSNPQSw)'s exported Chat data.

~Template data set is present [here](.). It holds all messages of [Devs Chat](https://t.me/joinchat/BkBvqUQUj4VKPmFSSNPQSw) upto _03/11/2019_ from initialization of group.~

**For respecting privacy of all users, I'm removing that data source from this public repo. Export chat data for your own need.**

### exporting chat
For exporting chat data for [Devs Chat](https://t.me/joinchat/BkBvqUQUj4VKPmFSSNPQSw) group of Telegram, I used Official Telegram Desktop Client. Exporting was done, while only including text messages _( no images, videos or audios )_, which are nothing but a bunch of HTML files.

If you want to run these scripts on your machine, make sure you've Telegram Desktop Client installed.

```shell script
$ sudo snap install telegram-desktop # run on your linux terminal
```
Log into your account and choose which chat to export. Well this expoting procedure can take some time, depending upon age & activeness of Chat.

## usage
Now you can directly install **tgnize** on your machine, using pip.
```shell script
$ pip3 install tgnize --user # make sure you've pip installed
```
[![asciicast](https://asciinema.org/a/zAm8En7JtEdft6qllfdTxfCys.svg)](https://asciinema.org/a/zAm8En7JtEdft6qllfdTxfCys)

Using **tgnize** is easy too, just pass path to directory, where you've exported Telegram Chat & sink directory path _( where generated plots to be stored )_
```bash
$ cd # at $HOME now
$ tgnize /path-to-exported-chat /sink-dir
[+]tgnize v0.1.3 - How about another Telegram Chat Analyzer ?

	$ tgnize `path-to-exported-chat-dir` `path-to-sink-dir`

[+]Author: Anjan Roy<anjanroy@yandex.com>
[+]Source: https://github.com/itzmeanjan/tgnize ( MIT Licensed )

[*]Preparing ...

[+]Options ::

	1 > Get Chat Participant Count
	2 > Get Message Count in Chat
	3 > Get Event Count in Chat
	4 > Get Total Activity Count in Chat
	5 > Get Top `X` Chat Participant(s)
	6 > Exit

tgnize >>

```

## progress

**This project is in its infancy, a lot of features to be added. If you've something in your mind, don't hesitate to create an issue or make a PR**

- [x] [Depiction of Accumulated Chat Traffic _( for whole Chat along with top **'X'** chat participants )_ with minute level details](./docs/minuteBasedAccumulatedTraffic.md)
- [x] [Top **'X'** Active Chat Participant(s) Over Time](./docs/topXActiveChatParticipantsOverTime.gif)
- [ ] Contribution of Chat Participants to Chat
- [ ] Overall Activity of Chat _( for a specified period of time )_
- [ ] Emoji Analysis
- [ ] Text Analysis

_Got some new idea ? Make a PR_ :wink:

**Work in Progress** - _coming with more details soon_
