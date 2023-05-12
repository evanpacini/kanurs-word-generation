#!/usr/bin/env python3
"""main.py: Generates random words using a Markov chain based on words from Google Sheets."""
__author__ = "Evan Pacini, Kasper van Maasdam"
__copyright__ = "Copyright 2023, Espersoft Inc."
__credits__ = ["Evan Pacini", "Kasper van Maasdam", "Timo de Kok", "Luke Kuijpers", "Lex Kuijpers"]

__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Evan Pacini, Kasper van Maasdam"
__email__ = "espersoft.inc@gmail.com"
__status__ = "Development"
__date__ = "12-05-2023"

import json
import os.path
import random

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
KANURS_ID = '1DjvktdD-oWmu6AAEPWWCdV3gQWpFJvmJzxEMMRGX5UM'
KANURS_RANGE = 'Words/Phrases!B2:B'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=KANURS_ID,
                                    range=KANURS_RANGE).execute()
        values = result.get('values', [])

        if not values:
            print('No data found in the sheets document.')
            return
        words = [word[0] for word in values if word != [] and ' ' not in word[0] and '-' not in word[0]]
        # back up words for offline use in json format
        with open('words_back_up.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(words))
        return words
    except:
        print('An error occurred while fetching data from Google Sheets.')
        return None


def build_markov_chain(data, n):
    """Build a markov chain from the given data and order.
    :param data: The data to build the markov chain from.
    :param n: The markov chain order.
    :return: The markov chain represented as a dictionary."""
    chain = {"initial": {}, "names": set(data)}
    for word in data:
        word_wrapped = str(word) + "."
        for i in range(len(word_wrapped) - n):
            item = word_wrapped[i: i + n]
            next_item = word_wrapped[i + 1: i + n + 1]

            if item in chain:
                entry = chain[item]
            else:
                entry = chain[item] = {}

            if i == 0:
                if item in chain["initial"]:
                    chain["initial"][item] += 1
                else:
                    chain["initial"][item] = 1

            if next_item in entry:
                entry[next_item] += 1
            else:
                entry[next_item] = 1
    return chain


def select_random_item(items):
    """Select a random item from the given dictionary of items.
    :param items: The dictionary of items to select from.
    :return: A random item from the dictionary."""
    rnd = random.random() * sum(items.values())
    for item in items:
        rnd -= items[item]
        if rnd < 0:
            return item


def generate(chain):
    """Generate a random item from the given markov chain.
    :param chain: The markov chain to generate from.
    :return: A random item generated from the markov chain."""
    item = select_random_item(chain["initial"])
    result = [item[:-1]]

    while item[-1] != ".":
        result.append(item[-1])
        item = select_random_item(chain[item])

    generated = "".join(result)
    if generated in chain["names"]:
        return generate(chain)
    return generated


links = main()
if links is None:
    print('Could not get newest data, so using last previous back-up.')
    try:
        with open('words_back_up.json', 'r', encoding='UTF-8') as f:
            links = eval(f.read())
    except IOError as err:
        print(f'Could not find any back-up data: {err}. Exiting.')
        exit(1)

markov_chain = build_markov_chain(links, 2)

print("Press enter to generate new words and type q to exit")
while input() != 'q':
    for _ in range(20):
        generated_word = generate(markov_chain)
        if generated_word not in links:
            print(generated_word)
