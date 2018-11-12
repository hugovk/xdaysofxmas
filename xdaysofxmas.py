#!/usr/bin/env python
# encoding: utf-8
"""
Christmas feels like it's starting earlier every year.

To celebrate, here are the lesser-known verses of the misnamed
Twelve Days of Christmas to get you in the spirit.

https://en.wikipedia.org/wiki/The_Twelve_Days_of_Christmas_(song)

Usage.

To generate 21 days of plain text:

python xdaysofxmas.py -d 21

To generate 50k+ words of HTML for NaNoGenMo 2015:

python xdaysofxmas.py -d 165 --html > output/xdaysofxmas.html
"""
from __future__ import print_function, unicode_literals

import argparse
import sys
from random import random, shuffle

import inflect  # pip install inflect
import yaml  # pip install pyyaml
from wordnik import WordsApi, swagger  # pip install wordnik

# from pprint import pprint

GIFTS = {
    1: "and a partridge in a pear tree.",
    2: "turtle doves",
    3: "French hens",
    4: "calling birds",
    5: "gold rings",
    6: "geese a-laying",
    7: "swans a-swimming",
    8: "maids a-milking",
    9: "ladies dancing",
    10: "lords a-leaping",
    11: "pipers piping",
    12: "drummers drumming",
}

TEMPLATE = "\nOn the {0} day of Christmas my true love sent to me:"

p = inflect.engine()

# Cache those lines we've already generated
cache = {}

print_html = False


def html(text, tag="br"):
    if print_html:
        if tag == "p":
            out = f"<{tag}>{text}"
        elif tag == "br":
            out = f"{text}<{tag}>"
        else:
            out = "<{0}>{1}</{0}>".format(tag, text)
    else:
        out = text
    print(out.encode("utf-8"))


def load_yaml(filename):
    """
    File should contain:
    wordnik_api_key: TODO_ENTER_YOURS
    """
    f = open(filename)
    data = yaml.safe_load(f)
    f.close()
    if not data.viewkeys() >= {"wordnik_api_key"}:
        sys.exit("Wordnik credentials missing from YAML: " + filename)
    return data


def get_random_words_from_wordnik(part_of_speech, limit):
    """ Get random words from Wordnik"""
    words = words_api.getRandomWords(includePartOfSpeech=part_of_speech, limit=limit)

    random_words = []
    for word in words:
        random_words.append(word.word)
    # pprint(random_words)
    return random_words


def a(noun):
    """If noun is plural, return 'noun'. Otherwise return 'a/an noun'"""
    if p.singular_noun(noun) is not False:
        return noun
    else:
        return p.a(noun)


def get_plural_nouns(how_many):
    nouns = get_random_words_from_wordnik("noun-plural", how_many)

    # If not enough noun-plural, top off with noun
    if len(nouns) < how_many:
        how_many_more = how_many - len(nouns)
        more_nouns = get_random_words_from_wordnik("noun", how_many_more)
        for noun in more_nouns:
            # Some of these are already plural and inflect is GIGO
            if noun.endswith("s") and not noun.endswith("ness"):
                nouns.append(noun)
            else:
                nouns.append(p.plural_noun(noun))

    assert len(nouns) == how_many
    shuffle(nouns)
    return nouns


def get_verbs(how_many):
    verbs = get_random_words_from_wordnik("verb-intransitive", how_many)

    # If not enough verb-intransitive, top off with verb-transitive
    if len(verbs) < how_many:
        how_many_more = how_many - len(verbs)
        more_verbs = get_random_words_from_wordnik("verb-transitive", how_many_more)
        verbs.extend(more_verbs)

    assert len(verbs) == how_many
    shuffle(verbs)
    return verbs


def get_pears(how_many):
    """These are either nouns or adjectives: the pear in pear tree"""
    pears = get_random_words_from_wordnik("noun", how_many / 2)
    pears2 = get_random_words_from_wordnik("adjective", how_many - len(pears))
    pears.extend(pears2)

    assert len(pears) == how_many
    shuffle(pears)
    return pears


def get_trees(how_many):
    """These are (ideally) singular nouns: the tree in pear tree"""
    trees = get_random_words_from_wordnik("noun", how_many)

    assert len(trees) == how_many
    shuffle(trees)
    return trees


def capify(text):
    """Uppercase the first letter"""
    return text[0].upper() + text[1:]


def gerundify(verb):
    """Hack -ing onto the end of a verb, and sometimes prefix a-"""
    if verb.endswith("e"):
        verb = verb[:-1]

    if random() < 0.4:
        if (
            not verb.startswith("a")
            and not verb.startswith("e")
            and not verb.startswith("i")
            and not verb.startswith("o")
            and not verb.startswith("u")
        ):
            verb = "a-" + verb

    return verb + "ing"


def giftify(day):
    """What gift for this day?"""
    index = day - 13
    if day < 13:
        gift = GIFTS[day]
    elif day % 10 == 1:
        # Partridge in a pear tree
        gift = plural_nouns[index] + " in " + a(pears.pop() + " " + trees.pop())
    elif day % 10 == 5:
        # Five gold rings
        gift = adjectives.pop() + " " + plural_nouns[index]
    else:
        gift = plural_nouns[index] + " " + gerundify(verbs.pop())
    if day > 1:
        gift = p.number_to_words(day) + " " + gift + ","

    gift = capify(gift)

    if print_html:
        if day != 11 and day % 10 == 1:
            # Partridge in a pear tree
            gift = "<i>" + gift + "</i>"
        elif day % 10 == 5:
            # Five gold rings
            gift = "<g>" + gift + "</g>"

    return gift


def from_cache(day):
    global cache

    try:
        line = cache[day]
    except KeyError:
        line = giftify(day)
        cache[day] = line

    return line


def partridge(days):
    global cache

    title = "The " + p.number_to_words(days).title() + " Days of Christmas"

    if print_html:
        print(
            """
<html>
<head>
  <meta charset="utf-8" />
  <title>{0} - NaNoGenMo2015</title>
  <link rel="stylesheet" type="text/css" href="xdaysofxmas.css">
  <link rel="shortcut icon" type="image/ico" href="favicon.ico"/>
</head>
<body>
<div id="snowflakeContainer">
  <p class="snowflake">*</p>
</div>

<h1>{0}</h1>

<h2 class="pagebreak">A generated songbook for NaNoGenMo 2015 by hugovk</h2>
""".format(
                title
            )
        )

    for day in range(1, days + 1):
        # print(day)
        # html(day, "h2")

        if print_html:
            print('<a href="#{0}"><h2 id="{0}">{0}</h2></a>'.format(day))

            if day % 2:
                odd_even = "even"
            else:
                odd_even = "odd"
            para = f'<P class="{odd_even}">'
            print(para)

        html(TEMPLATE.format(p.ordinal(p.number_to_words(day))), "br")
        for day2 in range(day, 0, -1):
            if day2 == 1:
                if day == 1:
                    line = from_cache(day2).replace("And a", "A")
                else:
                    line = from_cache(day2)
            else:
                line = from_cache(day2)
            html(line)

    if print_html:
        print(
            """
<script src="fallingsnow_v6.js"></script>
</body>
</html>"""
        )


def init_wordnik(yaml, days):
    global words_api, plural_nouns, pears, trees, verbs, adjectives

    credentials = load_yaml(yaml)
    wordnik_client = swagger.ApiClient(
        credentials["wordnik_api_key"], "http://api.wordnik.com/v4"
    )
    words_api = WordsApi.WordsApi(wordnik_client)

    how_many = days - 12
    plural_nouns = get_plural_nouns(how_many)
    how_many = int(days * 0.1) - 1 + 1
    pears = get_pears(how_many)
    trees = get_trees(how_many)
    # Don't need as many verbs or adjectives
    # 9 in 10 need verbs, but 11/12 are taken care of, and one for luck
    how_many = int(days * 0.9) - 11 + 1
    verbs = get_verbs(how_many)
    # 1 in 10 need adjectives, but 1/12 is taken care of, and one for luck
    how_many = int(days * 0.1) - 1 + 1
    adjectives = get_random_words_from_wordnik("adjective", how_many)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate the lesser-known verses of the misnamed "
        "Twelve Days of Christmas.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-d", "--days", type=int, help="How many days?")
    parser.add_argument(
        "-y",
        "--yaml",
        default="/Users/hugo/Dropbox/bin/data/wordnik.yaml",
        # default='M:/bin/data/wordnik.yaml',
        help="YAML file location containing Wordnik API key",
    )
    parser.add_argument("--html", action="store_true", help="HTML output")
    args = parser.parse_args()

    if args.html:
        print_html = True

    if args.days > 12:
        # Going to need some random words
        init_wordnik(args.yaml, args.days)

    partridge(args.days)

# End of file
