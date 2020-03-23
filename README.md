# human-zip

## What?

Human-readable text compression by repeated introduction of abbreviations.

## Why?

Is the book you want to read too long? Trying to save on printer paper? Or maybe you desperately need to fit your text to a page limit. 

Perhaps you put the document through a compression utility such as `zip`, `gzip`, or `7-zip` only to find that it outputs unreadable garbage?

*human-zip* is here to "help"!

## How?

`hzip.py` treats the input document as a string over an alphabet of words (i.e. words are characters). The working principle is similar to [Lempel-Ziv](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch) compression: common sequences of characters (phrases) are replaced with a new symbol (abbreviation) to compress the input. Unlike LZ compression, the output is human-readable and the "dictionary" is embedded into the text itself. 

The script computes a [suffix array](https://en.wikipedia.org/wiki/Suffix_array) and its longest common prefixes to find common repeated phrases. These phrases are scored based on length and number of occurrences, and an abbreviation is introduced for the top scoring phrase. 

Try for example: `python3 hzip.py never.txt`

## TODO

- [ ] Fix abbreviation collisions
- [ ] More efficient suffix array construction
- [ ] Deal with overlaps
- [ ] Handle common punctuation
- [ ] Handle plural words