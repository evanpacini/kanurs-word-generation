#!/usr/bin/env python3

import os.path
import random

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
            print('No data found.')
            return
        words = [word[0] for word in values if word != [] and ' ' not in word[0] and '-' not in word[0]]
        return words
    except HttpError as err:
        print(err)


def build_markov_chain(data, n):
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
    rnd = random.random() * sum(items.values())
    for item in items:
        rnd -= items[item]
        if rnd < 0:
            return item


def generate(chain):
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
markov_chain = build_markov_chain(links, 2)
while True:
    input()
    for _ in range(20):
        word = generate(markov_chain)
        if word not in links:
            print(word)
