"""McKinsey HTML Presentation Framework — High-level Layout Function Library.

Usage:
    from mck_html import MckHtmlEngine
    eng = MckHtmlEngine(total_slides=30)
    eng.cover(title='My Title', subtitle='Subtitle')
    eng.toc(items=[('1','Topic','Description'), ...])
    eng.save('output/my_deck.html')
"""
from .engine import MckHtmlEngine
from .constants import *

__version__ = '2.0.0'
