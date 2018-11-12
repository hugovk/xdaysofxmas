#!/usr/bin/env python
# encoding: utf-8
"""
On the Xth day of Christmas @MyTruLuvSent2Me
"""
from __future__ import print_function

import argparse
import datetime
import sys
import webbrowser

import twitter  # pip install twitter
import yaml  # pip install pyyaml
from wordnik import WordsApi, swagger  # pip install wordnik

import xdaysofxmas

# from pprint import pprint


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode('utf-8'))


def timestamp():
    """ Print a timestamp and the filename with path """
    print(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + " " +
          __file__)


def load_yaml(filename):
    """
    File should contain:
    consumer_key: TODO_ENTER_YOURS
    consumer_secret: TODO_ENTER_YOURS
    access_token: TODO_ENTER_YOURS
    access_token_secret: TODO_ENTER_YOURS
    wordnik_api_key: TODO_ENTER_YOURS
    """
    f = open(filename)
    data = yaml.safe_load(f)
    f.close()
    if not data.viewkeys() >= {
            'access_token', 'access_token_secret',
            'consumer_key', 'consumer_secret'}:
        sys.exit("Twitter credentials missing from YAML: " + filename)
    return data


def tweet_it(string, credentials, image=None):
    """ Tweet string and image using credentials """
    if len(string) <= 0:
        return

    # Create and authorise an app with (read and) write access at:
    # https://dev.twitter.com/apps/new
    # Store credentials in YAML file
    auth = twitter.OAuth(
        credentials['access_token'],
        credentials['access_token_secret'],
        credentials['consumer_key'],
        credentials['consumer_secret'])
    t = twitter.Twitter(auth=auth)

    print_it("TWEETING THIS:\n" + string)

    if args.test:
        print("(Test mode, not actually tweeting)")
    else:

        if image:
            print("Upload image")

            # Send images along with your tweets.
            # First just read images from the web or from files the regular way
            with open(image, "rb") as imagefile:
                imagedata = imagefile.read()
            t_up = twitter.Twitter(domain='upload.twitter.com', auth=auth)
            id_img = t_up.media.upload(media=imagedata)["media_id_string"]

            result = t.statuses.update(status=string, media_ids=id_img)
        else:
            result = t.statuses.update(status=string)

        url = "http://twitter.com/" + \
            result['user']['screen_name'] + "/status/" + result['id_str']
        print("Tweeted:\n" + url)
        if not args.no_web:
            webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


def day_of_chistmas():
    """Which day of Christmas?
    Christmas 2015 is the starting point.
    Return 1 for Christmas 2015.
    Return 2 for Boxing Day 2015, etc.
    """
    xmas = datetime.datetime(2015, 12, 25)
    print(xmas)
    now = datetime.datetime.now()
    print(now)

    diff = now - xmas

    print(diff.days)
    day = diff.days + 1
    print(day)
    return day


def giftify(day):
    """What gift for this day?"""
    if day < 13:
        gift = xdaysofxmas.GIFTS[day]
    elif day % 10 == 1:
        # Partridge in a pear tree
        plural_noun = xdaysofxmas.get_plural_nouns(1)[0]
        pear = xdaysofxmas.get_pears(20)[0]
        tree = xdaysofxmas.get_trees(1)[0]
        gift = plural_noun + " in " + xdaysofxmas.a(pear + " " + tree)
    elif day % 10 == 5:
        # Five gold rings
        adjective = xdaysofxmas.get_random_words_from_wordnik(
            "adjective", 1)[0]
        plural_noun = xdaysofxmas.get_plural_nouns(1)[0]
        gift = adjective + " " + plural_noun
    else:
        plural_noun = xdaysofxmas.get_plural_nouns(1)[0]
        verb = xdaysofxmas.get_verbs(1)[0]
        gift = plural_noun + " " + xdaysofxmas.gerundify(verb)
    if day > 1:
        gift = xdaysofxmas.p.number_to_words(day) + " " + gift + ","

    gift = xdaysofxmas.capify(gift)

    return gift


def screen_name(day):
    """On the xth day of Christmas... e.g. OnThe1stDayOfXmas"""
    # Your real name can be 20 characters long.
    while True:
        xth = xdaysofxmas.p.ordinal(day)
        name = f"OnThe{xth}DayOfXmas"
        if len(name) > 20:
            name = f"OnThe{day}DayOfXmas"
        elif len(name) <= 20:
            break
    return name


def update_screen_name(screen_name, credentials):
    """Update screen name on Twitter"""

    # TODO dedupe
    auth = twitter.OAuth(
        credentials['access_token'],
        credentials['access_token_secret'],
        credentials['consumer_key'],
        credentials['consumer_secret'])
    t = twitter.Twitter(auth=auth)

    if not args.test:
        t.account.update_profile(name=screen_name)


def timecheck():
    """Only run at certain hour"""
    if args.test:
        return

    utcnow = datetime.datetime.utcnow()

    # Only run at noon-ish UTC
    if utcnow.hour == 12:
        return
    else:
        exit()


if __name__ == "__main__":

    timestamp()

    parser = argparse.ArgumentParser(
        description="On the Xth day of Christmas @MyTruLuvSent2Me",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-y', '--yaml',
        default='/Users/hugo/Dropbox/bin/data/xdaysofxmasbot.yaml',
        # default='E:/Users/hugovk/Dropbox/bin/data/xdaysofxmasbot.yaml',
        help="YAML file location containing Twitter and Wordnik keys/secrets")
    parser.add_argument(
        '-nw', '--no-web', action='store_true',
        help="Don't open a web browser to show the tweeted tweet")
    parser.add_argument(
        '-x', '--test', action='store_true',
        help="Test mode: go through the motions but don't tweet anything")
    args = parser.parse_args()

    timecheck()

    credentials = load_yaml(args.yaml)

    day = day_of_chistmas()

    if day > 12:
        wordnik_client = swagger.ApiClient(credentials['wordnik_api_key'],
                                           'http://api.wordnik.com/v4')
        xdaysofxmas.words_api = WordsApi.WordsApi(wordnik_client)

    screen_name = screen_name(day)
    tweet = giftify(day)
    print(screen_name)
    print(tweet)

    update_screen_name(screen_name, credentials)
    tweet_it(tweet, credentials)

# End of file
