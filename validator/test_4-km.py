import pytest
from helper.km import *

#TODO: refactor:
#     - error msgs file
#     - non-blocking errors (more smaller tests)
#     - nicer code, easier to read (OOP?)


def test_load_chapters(chapters, km):
    for chapter in chapters.values():
        load_chapter(km, chapter)


def test_uuid_uniqueness(km):
    pass


def test_referencing(km):
    pass
