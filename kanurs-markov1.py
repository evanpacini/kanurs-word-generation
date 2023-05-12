#!/usr/bin/env python3
import random
import sys

def build_markov_chain(data, n):
    chain = {"initial": {}, "names": set(data)}
    for word in data:
        word_wrapped = str(word) + "."
        for i in range(len(word_wrapped) - n):
            tuple = word_wrapped[i: i + n]
            next = word_wrapped[i + 1: i + n + 1]

            if tuple in chain:
                entry = chain[tuple]
            else:
                entry = chain[tuple] = {}

            if i == 0:
                if tuple in chain["initial"]:
                    chain["initial"][tuple] += 1
                else:
                    chain["initial"][tuple] = 1

            if next in entry:
                entry[next] += 1
            else:
                entry[next] = 1
    return chain


def select_random_item(items):
    rnd = random.random() * sum(items.values())
    for item in items:
        rnd -= items[item]
        if rnd < 0:
            return item


def generate(chain):
    tuple = select_random_item(chain["initial"])
    result = [tuple[:-1]]

    while tuple[-1] != ".":
        result.append(tuple[-1])
        tuple = select_random_item(chain[tuple])

    generated = "".join(result)
    if generated in chain["names"]:
        return generate(chain)
    return generated


f = open("kanurs.txt", "r")
words = f.read().lower().splitlines()
chain = build_markov_chain(words, 2)
while True:
    input()
    for _ in range(20):
        print(generate(chain))
