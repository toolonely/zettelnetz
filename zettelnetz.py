#!/usr/bin/env python3

"""zettelnetz - stats about links between notes in a Zettelkasten

notes with zero references should be outline notes only

Usage: zettelnetz.py <directory>
"""

import os
import re
import string
import sys


NOTE_CHARS = set(string.ascii_lowercase) | set(string.digits) | set(["-"])
NOTE_NAME = r"\(([-a-z0-9]+\.md)\)"


def process_note(note):
    """
    Find links to other notes

    Args:
        note (str): note file name

    Return: list
    """
    links = []
    with open(note) as f:
        lines = f.readlines()
        for line in lines:
            match = re.search(NOTE_NAME, line)
            if match:
                link = match.group(1)
                links.append(link)
    return links


def num_links(note_record):
    """
    Key function for comparing note reference records

    Args:
        note_record (tuple): note record
    """
    return note_record[1]


def main():
    """main"""
    directory = sys.argv[1]
    all_files = os.listdir(directory)
    notes = [x for x in all_files
            if x[-3:] == ".md" and set(x[:-3]) <= NOTE_CHARS]
    note_references = {}
    for note in notes:
        links = process_note(os.path.join(directory, note))
        if note not in note_references:
            note_references[note] = 0
        for link in links:
            if link not in note_references:
                note_references[link] = 1
            else:
                note_references[link] += 1
    note_references_list = [(x, note_references[x]) for x in note_references]
    note_references_list.sort(key=num_links)
    for note_reference in note_references_list:
        print(note_reference[0], note_reference[1])


if __name__ == "__main__":
    main()
