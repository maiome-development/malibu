# -*- coding: utf-8 -*-
import random


__adjectives__ = [
    "adorable",
    "bigoted",
    "bouncy",
    "charming",
    "chipper",
    "comical",
    "crass",
    "creepy",
    "cross",
    "dangerous",
    "despressed",
    "diminished",
    "disfigured",
    "disturbed",
    "ecstatic",
    "electric",
    "enlightened",
    "excited",
    "failing",
    "faithful",
    "fastidious",
    "fervent",
    "firey",
    "flying",
    "frazzled",
    "freaky",
    "friendly",
    "frustrated",
    "gloomy",
    "glum",
    "gnarled",
    "gross",
    "hurtful",
    "immune",
    "intense",
    "jealous",
    "likable",
    "livid",
    "massive",
    "nasty",
    "naughty",
    "nosey",
    "offended",
    "overzealous",
    "peculiar",
    "perfunctory",
    "pleasant",
    "pokey",
    "pontiferous",
    "ravishing",
    "resourceful",
    "ridiculous",
    "riveting",
    "rowdy",
    "sad",
    "smashed",
    "smelly",
    "spectacular",
    "terrified",
    "voltaic",
]

__nouns__ = [
    "feynman", "einstein", "roadrunner", "tacocat", "grump", "fish",
    "michael", "bishop", "charlie", "metcalfe", "babbage", "zuckerberg",
    "nicholas", "priest", "doge", "pimp", "drone", "worker", "voltorb",
    "bulbasaur", "king", "bay", "transformers", "johnson", "baby",
    "charmander", "mew", "axel", "wayne", "charles", "jessica", "clarice",
    "doctor", "horton", "ballmer", "jobs", "gates", "failfish"
]


def get_simple_name(delim='_'):

    adj = random.choice(__adjectives__)
    noun = random.choice(__nouns__)

    return delim.join([adj, noun])


def get_complex_name(num_adjs=1, num_nouns=1, delim='_'):

    adjs = [random.choice(__adjectives__) for i in range(num_adjs)]
    nouns = [random.choice(__nouns__) for i in range(num_nouns)]

    adjs.extend(nouns)

    return delim.join(adjs)
