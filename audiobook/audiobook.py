#!/usr/bin/env python
# encoding: utf-8
"""
Makes an audiobook of The One Hundred And Sixty-Five Days of Christmas.

Requires OS X's say command, also sox and ffmpeg.
"""
from __future__ import print_function, unicode_literals

import os
from random import choice

import inflect  # pip install inflect

VOICES = [
    "Agnes",
    "Albert",
    "Alex",
    "Alice",
    "Alva",
    "Amelie",
    "Anna",
    "Bad News",
    "Bahh",
    "Bells",
    "Boing",
    "Bruce",
    "Bubbles",
    "Carmit",
    "Cellos",
    "Damayanti",
    "Daniel",
    "Deranged",
    "Diego",
    "Ellen",
    "Fiona",
    "Fred",
    "Good News",
    "Hysterical",
    "Ioana",
    "Joana",
    "Junior",
    "Kanya",
    "Karen",
    "Kathy",
    "Kyoko",
    "Laura",
    "Lekha",
    "Luciana",
    "Maged",
    "Mariska",
    "Mei-Jia",
    "Melina",
    "Milena",
    "Moira",
    "Monica",
    "Nora",
    "Paulina",
    "Pipe Organ",
    "Princess",
    "Ralph",
    "Samantha",
    "Sara",
    "Satu",
    "Sin-ji",
    "Tessa",
    "Thomas",
    "Ting-Ting",
    "Trinoids",
    "Veena",
    "Vicki",
    "Victoria",
    "Whisper",
    "Xander",
    "Yelda",
    "Yuna",
    "Zarvox",
    "Zosia",
    "Zuzana",
]

LINES = [
    "One hundred and sixty-five browner Manirul,",
    "One hundred and sixty-four nephilim a-spooming,",
    "One hundred and sixty-three rattlings menging,",
    "One hundred and sixty-two praecognita a-self-actualizing,",
    "One hundred and sixty-one oblati in crackpottery Santas,",
    "One hundred and sixty striges underreacting,",
    "One hundred and fifty-nine rugosa bracketing,",
    "One hundred and fifty-eight Occidentals dimpling,",
    "One hundred and fifty-seven Belgae chesing,",
    "One hundred and fifty-six persiennes configurating,",
    "One hundred and fifty-five chthonian lesses,",
    "One hundred and fifty-four letts assassining,",
    "One hundred and fifty-three gallinaceae neesing,",
    "One hundred and fifty-two clayes enthroning,",
    "One hundred and fifty-one labras in an incomplex chunnel,",
    "One hundred and fifty pecora a-proaching,",
    "One hundred and forty-nine negritos whooting,",
    "One hundred and forty-eight herbivora allegorizing,",
    "One hundred and forty-seven pettitoes a-squawling,",
    "One hundred and forty-six Volsci scringing,",
    "One hundred and forty-five cognizable appendiculata,",
    "One hundred and forty-four vermes a-perissing,",
    "One hundred and forty-three fifth-starter gormandizing,",
    "One hundred and forty-two brachyptera job-sharing,",
    "One hundred and forty-one dagges in a tradelines turner,",
    "One hundred and forty standing-o deprecating,",
    "One hundred and thirty-nine seven-thirties a-reembracing,",
    "One hundred and thirty-eight annulosa a-self-sowing,",
    "One hundred and thirty-seven lemures lipsing,",
    "One hundred and thirty-six conchifera a-cicatrizing,",
    "One hundred and thirty-five conflictful annulata,",
    "One hundred and thirty-four radiata a-faddling,",
    "One hundred and thirty-three ramenta unpredicting,",
    "One hundred and thirty-two Seawright slattering,",
    "One hundred and thirty-one crees in a Hemingwayesque orphrey,",
    "One hundred and thirty perforata evanishing,",
    "One hundred and twenty-nine emerods a-cleansing,",
    "One hundred and twenty-eight acephala ventriloquizing,",
    "One hundred and twenty-seven reliquiae a-fenerating,",
    "One hundred and twenty-six dragées entending,",
    "One hundred and twenty-five constitutional dinosauria,",
    "One hundred and twenty-four pearlins a-knowledging,",
    "One hundred and twenty-three apoda recching,",
    "One hundred and twenty-two oreades sippling,",
    "One hundred and twenty-one Penates in a germier Pukapuka,",
    "One hundred and twenty amphictyons hoseying,",
    "One hundred and nineteen Gastrotricha a-tabering,",
    "One hundred and eighteen Bacchae belly-landing,",
    "One hundred and seventeen tabulata a-doxologizing,",
    "One hundred and sixteen principia rooster-tailing,",
    "One hundred and fifteen geolocative silvas,",
    "One hundred and fourteen ferae a-kithing,",
    "One hundred and thirteen Vestales charming,",
    "One hundred and twelve cates unruffling,",
    "One hundred and eleven dalles in an unmeasured sidearmer,",
    "One hundred and ten cursores industrializing,",
    "One hundred and nine Kauravas obtaining,",
    "One hundred and eight picts enviing,",
    "One hundred and seven fioriture a-rapining,",
    "One hundred and six pentecostals outstarting,",
    "One hundred and five hemopoietic stives,",
    "One hundred and four quadrumana water-skiing,",
    "One hundred and three fleen self-seeding,",
    "One hundred and two lazaroni preceding,",
    "One hundred and one Urodela in a sunstrokes thermopower,",
    "One hundred gerontes provining,",
    "Ninety-nine Cherokees auto-destructing,",
    "Ninety-eight Helvetii spanging,",
    "Ninety-seven spatterdashes dreining,",
    "Ninety-six rapilli a-disserting,",
    "Ninety-five longtailed grallatores,",
    "Ninety-four gwyllt a-loffing,",
    "Ninety-three Also-Rans rollicing,",
    "Ninety-two secundines discussing,",
    "Ninety-one ovipara in heterozygous grapefruits,",
    "Ninety jears a-plucking,",
    "Eighty-nine top-boots swashbuckling,",
    "Eighty-eight Iceni nose-diving,",
    "Eighty-seven gaskins upbearing,",
    "Eighty-six shakings reprising,",
    "Eighty-five melliferous pachydermata,",
    "Eighty-four curriculae cheving,",
    "Eighty-three thummim reassembling,",
    "Eighty-two fal-lals fore-checking,",
    "Eighty-one inexpressibles in davits pleuritis,",
    "Eighty psittaci confedering,",
    "Seventy-nine scatches mouling,",
    "Seventy-eight Alemanni a-womanizing,",
    "Seventy-seven iowas a-tumultuating,",
    "Seventy-six blackfeet fletching,",
    "Seventy-five miscolored synonyma,",
    "Seventy-four Smalls a-rangling,",
    "Seventy-three jugata overbriming,",
    "Seventy-two kemps a-greiting,",
    "Seventy-one rapaces in a mutism milliamp,",
    "Seventy helminthes upstanding,",
    "Sixty-nine Egesta fugling,",
    "Sixty-eight populares sourding,",
    "Sixty-seven senecas a-rebellowing,",
    "Sixty-six sowens insurrecting,",
    "Sixty-five non-enzymatic vibices,",
    "Sixty-four columbae back-checking,",
    "Sixty-three cruels swarving,",
    "Sixty-two jython a-ligging,",
    "Sixty-one rubaiyat in throughgoing sheats,",
    "Sixty fasti evesdroping,",
    "Fifty-nine techo a-persevering,",
    "Fifty-eight invertebrata ziggering,",
    "Fifty-seven delawares a-compearing,",
    "Fifty-six graveclothes insuing,",
    "Fifty-five patchier platypoda,",
    "Fifty-four cerealia freebooting,",
    "Fifty-three dejecta a-traditioning,",
    "Fifty-two delenda recapitulating,",
    "Fifty-one loups in an antisodomy lurdane,",
    "Fifty navals schismatizing,",
    "Forty-nine estovers hotching,",
    "Forty-eight jambes a-cantiling,",
    "Forty-seven piatti a-condoging,",
    "Forty-six squali curating,",
    "Forty-five riper pedunculata,",
    "Forty-four notabilia gelating,",
    "Forty-three Danaides unretiring,",
    "Forty-two fantoccini upswelling,",
    "Forty-one middlings in gasometric paper-knives,",
    "Forty post-delivery a-requering,",
    "Thirty-nine illuminati a-diffiding,",
    "Thirty-eight five-twenties experimentalizing,",
    "Thirty-seven Lauper's disceding,",
    "Thirty-six pedata smudging,",
    "Thirty-five splashproof sowins,",
    "Thirty-four abdominales interpleading,",
    "Thirty-three entozoa whirrying,",
    "Thirty-two burnsides a-remerging,",
    "Thirty-one quirites in a monometallism glycopyrrolate,",
    "Thirty spraints congreing,",
    "Twenty-nine gamashes ego-triping,",
    "Twenty-eight articulata a-congruing,",
    "Twenty-seven smarty-pants a-merchanding,",
    "Twenty-six craniota gayning,",
    "Twenty-five undealt annats,",
    "Twenty-four aptera a-visiting,",
    "Twenty-three disparates a-proking,",
    "Twenty-two vivers play-acting,",
    "Twenty-one diurna in a nanomotor salley,",
    "Twenty judaizers a-dipsy-doodling,",
    "Nineteen antilegomena gleening,",
    "Eighteen Fascisti a-deducing,",
    "Seventeen rurales a-job-hunting,",
    "Sixteen Arrey a-tub-thumping,",
    "Fifteen visored outbounds,",
    "Fourteen nowes relucting,",
    "Thirteen tetramera readvancing,",
    "Twelve drummers drumming,",
    "Eleven pipers piping,",
    "Ten lords a-leaping,",
    "Nine ladies dancing,",
    "Eight maids a-milking,",
    "Seven swans a-swimming,",
    "Six geese a-laying,",
    "Five gold rings,",
    "Four calling birds,",
    "Three French hens,",
    "Two turtle doves,",
    "And a partridge in a pear tree.",
]


print(len(LINES))


def run(cmd):
    print(cmd)
    os.system(cmd.encode("utf-8"))


# First gen audio lines

p = inflect.engine()

last_voice = None
for i, line in enumerate(reversed(LINES)):
    voice = choice(VOICES)
    while last_voice == voice:
        voice = choice(VOICES)
    last_voice = voice

    # Intro
    txt = "On the {} day of Christmas my true love sent to me".format(
        p.ordinal(p.number_to_words(i + 1))
    )
    cmd = 'say -v {} "{}" -o intro-{:03d}.aiff'.format(voice, txt, i + 1)
    run(cmd)

    cmd = 'say -v {} "{}" -o line-{:03d}.aiff'.format(voice, line, i + 1)
    run(cmd)

    # Special case for first day
    if i == 0:
        line = line.replace("And a", "A")
        cmd = 'say -v "{}" "{}" -o line-{:03d}-first.aiff'.format(voice, line, i + 1)
        run(cmd)


# Next assemble

for i in range(len(LINES) - 1, -1, -1):
    print(i)
    input = "intro-{:03d}.aiff".format(i + 1)
    for j in range(i, -1, -1):
        input += " line-{:03d}.aiff".format(j + 1)

    output = "verse-{:03d}.aiff".format(i + 1)

    # Special case for first day
    if i == 0:
        print(112)
        print(input)
        input = input.replace("line-001.aiff", "line-001-first.aiff")
        print(input)

    # Join 'em
    cmd = f"sox {input} {output}"
    run(cmd)

    # Remove some old aiffs
    cmd = "rm intro-{0:03d}.aiff line-{0:03d}.aiff ".format(i + 1)
    run(cmd)

    # Compress to mp3
    input = "verse-{:03d}.aiff".format(i + 1)
    output = input.replace(".aiff", ".mp3")
    cmd = f"ffmpeg -i {input} {output}"
    run(cmd)

# Delete some old aiffs
cmd = "rm intro-*.aiff line-*.aiff"
run(cmd)

# Make one big, final audiobook
input = ""
for i in range(len(LINES)):
    input += " verse-{:03d}.aiff".format(i + 1)
output = "audiobook.aiff"
cmd = f"sox {input} {output}"
run(cmd)
cmd = "ffmpeg -i audiobook.aiff audiobook.mp3"
run(cmd)

# Delete rest of old aiffs
cmd = "rm *.aiff"
run(cmd)

# End of file
