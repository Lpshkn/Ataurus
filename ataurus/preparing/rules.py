"""
Module contains the regex rules that will be used during processing text
in the preparator.py module.
"""
import re
from razdel.segmenters.tokenize import PUNCTS


PUNCTUATIONS = re.compile(f"[%s]" % re.escape(PUNCTS))
LINKS = re.compile(r"(https?://[^\s]+)|(www\.[^\s]+)")
